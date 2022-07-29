from datetime import timedelta
from typing import Union

from requests.adapters import HTTPAdapter

from featureprobe.internal.defaultable import defaultable


@defaultable
class HttpConfig:
    def __init__(self,
                 pool_connections: int = 5,
                 pool_maxsize: int = 10,
                 conn_timeout: Union[timedelta, float] = timedelta(seconds=3),
                 read_timeout: Union[timedelta, float] = timedelta(seconds=3)):
        self.conn_timeout = conn_timeout.total_seconds() \
            if isinstance(conn_timeout, timedelta) \
            else conn_timeout
        self.read_timeout = read_timeout.total_seconds() \
            if isinstance(read_timeout, timedelta) \
            else read_timeout
        self.adapter = HTTPAdapter(
            pool_maxsize=pool_maxsize,
            pool_connections=pool_connections,
            max_retries=0,
        )
