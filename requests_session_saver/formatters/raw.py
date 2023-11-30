import requests


class RawFormatter:
    file_extension = "raw"

    def export_request(self, request: requests.PreparedRequest) -> str:
        return ""

    def export_response(self, response: requests.Response) -> str:
        return ""
