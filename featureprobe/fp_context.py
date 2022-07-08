import logging

from fp_config import FPConfig


class FPContext:
    __logger = logging.getLogger('FeatureProbe')
    __GET_REPOSITORY_DATA_API = '/api/server-sdk/toggles'
    __POST_EVENTS_DATA_API = '/api/events'

    def __init__(self, server_sdk_key: str, config: FPConfig):
        self._synchronizer_url = config.synchronizer_url or config.remote_uri + FPContext.__GET_REPOSITORY_DATA_API
        self._event_url = config.event_url or config.remote_uri + FPContext.__POST_EVENTS_DATA_API
        self._server_sdk_key = server_sdk_key
        self._refresh_interval = config.refresh_interval
        self._location = config.location
        self._http_configuration = config.http_configuration

    @property
    def synchronizer_url(self):
        return self._synchronizer_url

    @property
    def event_url(self):
        return self._event_url

    @property
    def server_sdk_key(self):
        return self._server_sdk_key

    @property
    def refresh_interval(self):
        return self._refresh_interval

    @property
    def location(self):
        return self._location

    @property
    def http_configuration(self):
        return self._http_configuration
