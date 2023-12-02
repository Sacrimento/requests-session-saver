import json
from typing import Any, Union
from urllib.parse import urlparse

import requests


class JsonFormatter:
    file_extension = "json"

    def _try_body_as_json(self, body: Union[str, bytes, None]) -> Any:
        if not body:
            return body

        try:
            return json.loads(body)
        except json.JSONDecodeError:
            return body

    def format_request(self, request: requests.PreparedRequest) -> str:
        url_comps = urlparse(request.url)

        path = str(url_comps.path)
        if url_comps.query:
            path += f"?{url_comps.query!s}"

        obj = {
            "meta": {"verb": request.method, "path": path, "http_version": "HTTP/1.1"},
            "headers": request.headers,
            "body": self._try_body_as_json(request.body),
        }
        return json.dumps(obj, indent=4)

    def format_response(self, response: requests.Response) -> str:
        http_version = ".".join(str(response.raw.version))

        obj = {
            "meta": {
                "http_version": f"HTTP/{http_version}",
                "status": response.status_code,
                "reason": response.reason,
            },
            "headers": response.headers,
            "body": self._try_body_as_json(response.text),
        }
        return json.dumps(obj, indent=4)
