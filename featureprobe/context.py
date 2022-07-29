from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from featureprobe.config import Config


class Context:
    _GET_REPOSITORY_DATA_API = '/api/server-sdk/toggles'
    _POST_EVENTS_DATA_API = '/api/events'

    def __init__(self, sdk_key: str, config: "Config"):
        self._synchronizer_url = config.synchronizer_url or (config.remote_uri + self._GET_REPOSITORY_DATA_API)
        self._event_url = config.event_url or (config.remote_uri + self._POST_EVENTS_DATA_API)
        self._sdk_key = sdk_key
        self._refresh_interval = config.refresh_interval
        self._location = config.location
        self._http_config = config.http_config

    @property
    def synchronizer_url(self):
        return self._synchronizer_url

    @property
    def event_url(self):
        return self._event_url

    @property
    def sdk_key(self):
        return self._sdk_key

    @property
    def refresh_interval(self):
        return self._refresh_interval

    @property
    def location(self):
        return self._location

    @property
    def http_config(self):
        return self._http_config
