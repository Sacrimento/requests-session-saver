import requests


class JsonFormatter:
    file_extension = "json"

    def format_request(self, request: requests.PreparedRequest) -> str:
        return ""

    def format_response(self, response: requests.Response) -> str:
        return ""
