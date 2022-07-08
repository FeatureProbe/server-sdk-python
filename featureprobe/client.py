import json
import logging
import time
from typing import Any

from event import AccessEvent
from fp_config import FPConfig
from fp_context import FPContext
from fp_detail import FPDetail
from fp_user import FPUser


class Client:
    __logger = logging.getLogger('FeatureProbe')

    def __init__(self, sdk_key: str, config: FPConfig = FPConfig()):
        if not sdk_key:
            raise ValueError('sdk key must not be blank')
        context = FPContext(sdk_key, config)
        self._event_processor = config.event_processor_factory.create(context)
        self._data_repo = config.data_repository_factory.create(context)
        config.synchronizer_factory.create(context, self._data_repo).sync()

    def flush(self):
        self._event_processor.flush()

    def evaluate(self, toggle_key: str, user: FPUser, default, is_json: bool) -> Any:
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
        if is_json:
            ...
            # FIXME
            """
            return mapper.readValue(value, clazz);
                }
            } catch (JsonProcessingException e) {
                logger.error(LOG_CONVERSION_ERROR, toggleKey, e);
            } catch (Exception e) {
                logger.error(LOG_HANDLE_ERROR, toggleKey, e);
            }
            """

            #     public <T> T jsonValue(String toggleKey, FPUser user, T defaultValue, Class<T> clazz) {
            #         return jsonEvaluate(toggleKey, user, defaultValue, clazz);
            #     }

        else:
            return eval_result.value

    def evaluate_detail(self, toggle_key: str, user: FPUser, default, is_json: bool) -> FPDetail:
        if not self._data_repo.initialized:
            return FPDetail(value=default, reason='FeatureProbe repository uninitialized')

        toggle = self._data_repo.get_toggle(toggle_key)
        segments = self._data_repo.get_all_segment()

        if not toggle:  # toggle is null
            return FPDetail(value=default, reason='Toggle not exist')

        eval_result = toggle.eval(user, segments, default)
        detail = FPDetail(value=json.dumps(eval_result.value) if is_json else eval_result.value,
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
