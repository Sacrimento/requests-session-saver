import requests


class RawFormatter:
    file_extension = "raw"

    def format_request(self, request: requests.PreparedRequest) -> str:
        return ""

    def format_response(self, response: requests.Response) -> str:
        return ""
