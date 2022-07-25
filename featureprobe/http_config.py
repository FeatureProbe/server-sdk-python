from datetime import timedelta
from typing import Union

import aiohttp

from internal.defaultable import defaultable


@defaultable
class HttpConfig:
    def __init__(self,
                 pool_connections: int = 5,
                 conn_timeout: Union[timedelta, float] = timedelta(seconds=3),
                 read_timeout: Union[timedelta, float] = timedelta(seconds=3),
                 write_timeout: Union[timedelta, float] = timedelta(seconds=3),
                 keepalive_timeout: Union[timedelta, float] = timedelta(seconds=5)):
        self.conn_timeout = conn_timeout.total_seconds() \
            if isinstance(conn_timeout, timedelta) \
            else conn_timeout
        self.read_timeout = read_timeout.total_seconds() \
            if isinstance(read_timeout, timedelta) \
            else read_timeout
        self.write_timeout = write_timeout.total_seconds() \
            if isinstance(write_timeout, timedelta) \
            else write_timeout
        keepalive_timeout = keepalive_timeout.total_seconds() \
            if isinstance(keepalive_timeout, timedelta) \
            else keepalive_timeout
        self.connector = aiohttp.TCPConnector(
            ssl=False,
            limit=pool_connections,
            keepalive_timeout=keepalive_timeout,
            enable_cleanup_closed=True
        )
