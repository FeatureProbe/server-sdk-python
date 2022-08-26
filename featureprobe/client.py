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

import logging
import time
from typing import Any

from featureprobe.config import Config
from featureprobe.context import Context
from featureprobe.detail import Detail
from featureprobe.event import AccessEvent
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
        self._synchronizer = config.synchronizer_creator(
            context, self._data_repo)
        self._synchronizer.sync()

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
        if not toggle:
            return default

        eval_result = toggle.eval(user, segments, default)
        access_event = AccessEvent(timestamp=int(time.time() * 1000),
                                   user=user,
                                   key=toggle_key,
                                   value=str(eval_result.value),
                                   version=eval_result.version,
                                   index=eval_result.variation_index)
        self._event_processor.push(access_event)
        return eval_result.value

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

        if toggle is None:
            return Detail(value=default, reason='Toggle not exist')

        eval_result = toggle.eval(user, segments, default)
        detail = Detail(value=eval_result.value,
                        reason=eval_result.reason,
                        rule_index=eval_result.rule_index,
                        version=eval_result.version)
        access_event = AccessEvent(timestamp=int(time.time() * 1000),
                                   user=user,
                                   key=toggle_key,
                                   value=eval_result.value,
                                   version=eval_result.version,
                                   index=eval_result.variation_index)
        self._event_processor.push(access_event)
        return detail
