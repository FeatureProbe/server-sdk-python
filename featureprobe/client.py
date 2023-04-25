# Copyright 2022 FeatureProbe
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Optional
import logging
import time
from threading import Event
from typing import Any

from featureprobe.config import Config
from featureprobe.context import Context
from featureprobe.detail import Detail
from featureprobe.event import AccessEvent, CustomEvent, DebugEvent
from featureprobe.internal.empty_str import empty_str
from featureprobe.user import User


class Client:
    """A client for the FeatureProbe API. Client instances are thread-safe.

    Applications should instantiate a single :obj:`~featureprobe.Client` for the lifetime of their application.
    """

    __logger = logging.getLogger('FeatureProbe')

    def __init__(self, server_sdk_key: str, config: Config = Config()):
        """Creates a new client instance that connects to FeatureProbe with the default configuration.

        :param server_sdk_key: Server SDK Key for your FeatureProbe environment.
        :param config: (optional) The configuration control FeatureProbe client behavior.
                        Leaving this argument unfilled will use the default configuration.
        """
        if empty_str(server_sdk_key):
            raise ValueError('sdk key must not be blank')
        context = Context(server_sdk_key, config)
        self._event_processor = config.event_processor_creator(context)
        self._data_repo = config.data_repository_creator(context)
        self._config = config

        synchronize_process_ready = Event()
        self._synchronizer = config.synchronizer_creator(
            context, self._data_repo, synchronize_process_ready)
        self._synchronizer.start()
        if config.start_wait > 0:
            Client.__logger.info("Waiting up to " +
                                 str(config.start_wait) +
                                 " seconds for FeatureProbe client to initialize...")
            synchronize_process_ready.wait(config.start_wait)
        if self._synchronizer.initialized() is True:
            Client.__logger.info("Started FeatureProbe Client: Successfully")
        else:
            Client.__logger.warning(
                "Initialization timeout exceeded for FeatureProbe Client or an error occurred")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Alias for :func:`~featureprobe.Client.close`

        Usage::

          >>> import featureprobe as fp
          >>> with fp.Client('key_000') as client:
          >>>     ...
          >>> # client will be closed here
        """
        self.close()

    def initialized(self):
        """Tests whether the FeatureProbe client is ready to be used"""
        return self._synchronizer.initialized()

    def flush(self):
        """Manually push events"""
        self._event_processor.flush()

    def close(self):
        """Safely shut down FeatureProbe client instance"""
        Client.__logger.info('Closing FeatureProbe Client')
        self._event_processor.shutdown()
        self._synchronizer.close()
        self._data_repo.close()

    def value(self, toggle_key: str, user: User, default) -> Any:
        """Gets the evaluated value of a toggle.

        :param toggle_key: The key of toggle in this environment.
        :param user: :obj:`~featureprobe.User` to be evaluated.
        :param default: The default value to be returned.
        :returns: Dependents on the toggle's type.
        """
        toggle = self._data_repo.get_toggle(toggle_key)
        segments = self._data_repo.get_all_segment()
        toggles = self._data_repo.get_all_toggle()
        if not toggle:
            return default

        eval_result = toggle.eval(
            user,
            toggles,
            segments,
            default,
            self._config.max_prerequisites_deep)
        self._track_event(user, toggle, eval_result)
        return eval_result.value

    def _track_event(self, user, toggle, eval_result):
        current_time_millis = int(time.time() * 1000)
        access_event = AccessEvent(
            timestamp=current_time_millis,
            user=user,
            key=toggle.key,
            value=eval_result.value,
            version=eval_result.version,
            variation_index=eval_result.variation_index,
            track_access_events=toggle.track_access_events)
        self._event_processor.push(access_event)
        if self._should_debug_event(current_time_millis):
            debug_event = DebugEvent(
                timestamp=current_time_millis,
                user=user,
                key=toggle.key,
                value=eval_result.value,
                version=eval_result.version,
                variation_index=eval_result.variation_index,
                rule_index=eval_result.rule_index,
                reason=eval_result.reason)
            self._event_processor.push(debug_event)

    def _should_debug_event(self, current_time_millis):
        debug_until_time = self._data_repo.get_debug_until_time()
        return debug_until_time is not None and debug_until_time > current_time_millis
        
    def value_detail(self, toggle_key: str, user: User, default) -> Detail:
        """Gets the detailed evaluated results of a toggle.

        :param toggle_key: The key of toggle in this environment.
        :param user: :obj:`~featureprobe.User` to be evaluated.
        :param default: The default value to be returned.
        :returns: :obj:`~featureprobe.Detail` contains the `value`, `rule_index`, `version`, and `reason`
                  of this evaluation.
        """

        if not self._data_repo.initialized:
            return Detail(
                value=default,
                reason='FeatureProbe repository uninitialized')

        toggle = self._data_repo.get_toggle(toggle_key)
        segments = self._data_repo.get_all_segment()
        toggles = self._data_repo.get_all_toggle()

        if toggle is None:
            return Detail(value=default, reason='Toggle not exist')

        eval_result = toggle.eval(
            user,
            toggles,
            segments,
            default,
            self._config.max_prerequisites_deep)
        detail = Detail(value=eval_result.value,
                        reason=eval_result.reason,
                        rule_index=eval_result.rule_index,
                        version=eval_result.version)
        self._track_event(user, toggle, eval_result)

        return detail

    def track(
            self,
            event_name: str,
            user: User,
            value: Optional[float] = None):
        """Tracks that a custom defined event

        :param event_name: the name of the event.
        :param user: :obj:`~featureprobe.User` to be evaluated.
        :param value: a numeric value(Optional).
        """
        self._event_processor.push(
            CustomEvent(
                timestamp=int(
                    time.time() * 1000),
                name=event_name,
                user=user,
                value=value))
