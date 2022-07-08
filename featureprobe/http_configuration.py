import aiohttp

from internal.wrapper_default import defaultable


@defaultable
class HttpConfiguration:

    def __init__(self,
                 conn_timeout=3000,
                 read_timeout=3000,
                 write_timeout=3000,
                 pool_connections:int=5,
                 keepalive_timeout=5):
        self.conn_timeout = conn_timeout
        self.read_timeout = read_timeout
        self.write_timeout = write_timeout
        self.connector = aiohttp.TCPConnector(
            verify_ssl=False,
            limit=pool_connections,
            keepalive_timeout=keepalive_timeout,
            enable_cleanup_closed=True
        )

    # FIXME: ensure unit: sec ? millisec