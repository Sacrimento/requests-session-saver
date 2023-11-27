import requests


class RawExporter:
    def export_request(self, request: requests.PreparedRequest) -> str:
        return ""

    def export_response(self, response: requests.Response) -> str:
        return ""
