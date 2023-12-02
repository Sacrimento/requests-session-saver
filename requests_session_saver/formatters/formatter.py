from typing import Protocol

import requests


class Formatter(Protocol):
    def format_request(self, request: requests.PreparedRequest) -> str:
        ...

    def format_response(self, response: requests.Response) -> str:
        ...
