import socket
from contextlib import closing


class MockHttpReponse:
    def __init__(self, status_code, json_response):
        self.status_code = status_code
        self.response = json_response

    def raise_for_status(self):
        pass

    def json(self):
        return self.response


def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(("", 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]
