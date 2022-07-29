import time
from typing import Any

from featureprobe.config import Config
from featureprobe.context import Context
from featureprobe.detail import Detail
from featureprobe.event import AccessEvent
from featureprobe.internal.empty_str import empty_str
from featureprobe.user import User


class Sdk:
    def __init__(self, sdk_key: str, config: Config = Config()):
        if empty_str(sdk_key):
            raise ValueError('sdk key must not be blank')
        context = Context(sdk_key, config)
        self._event_processor = config.event_processor_creator(context)
        self._data_repo = config.data_repository_creator(context)
        config.synchronizer_creator(context, self._data_repo).sync()

    def flush(self):
        self._event_processor.flush()

    def evaluate(self, toggle_key: str, user: User, default) -> Any:
        toggle = self._data_repo.get_toggle(toggle_key)
        segments = self._data_repo.get_all_segment()
        if not toggle:
            return default

        eval_result = toggle.eval(user, segments, default)
        access_event = AccessEvent(timestamp=int(time.time()),
                                   user=user,
                                   key=toggle_key,
                                   value=str(eval_result.value),
                                   version=eval_result.version,
                                   index=eval_result.variation_index)
        self._event_processor.push(access_event)
        return eval_result.value

    def evaluate_detail(self, toggle_key: str, user: User, default) -> Detail:
        if not self._data_repo.initialized:
            return Detail(value=default, reason='FeatureProbe repository uninitialized')

        toggle = self._data_repo.get_toggle(toggle_key)
        segments = self._data_repo.get_all_segment()

        if toggle is None:
            return Detail(value=default, reason='Toggle not exist')

        eval_result = toggle.eval(user, segments, default)
        detail = Detail(value=eval_result.value,
                        reason=eval_result.reason,
                        rule_index=eval_result.rule_index,
                        version=eval_result.version)
        access_event = AccessEvent(timestamp=int(time.time()),
                                   user=user,
                                   key=toggle_key,
                                   value=eval_result.value,
                                   version=eval_result.version,
                                   index=eval_result.variation_index)
        self._event_processor.push(access_event)
        return detail
