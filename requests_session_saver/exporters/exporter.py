from typing import Protocol

import requests


class Exporter(Protocol):
    def export_request(self, request: requests.PreparedRequest) -> str:
        ...

    def export_response(self, response: requests.Response) -> str:
        ...
