from pathlib import Path
import tempfile
from typing import Type, Union
from urllib.parse import urlparse

import requests

from .formatters import BUILTIN_FORMATTERS, Formatter

DEFAULT_FORMATTER = "JSON"


class SessionSaver:
    def __init__(
        self,
        session: requests.Session,  # TODO Intercept everything if no session?
        /,
        directory: Union[Path, None] = None,
        formatter: Union[Type[Formatter], str, None] = None,
    ) -> None:
        self.dir = self._get_work_dir(directory)
        self.formatter = self._get_formatter(formatter)
        self.req_count = 0

        session.hooks["response"].append(self.save)

    def _get_work_dir(self, directory: Union[Path, None]) -> Path:
        if directory is None:
            return Path(tempfile.mkdtemp())

        if directory.exists():
            if not directory.is_dir():
                raise ValueError(f"{directory} is not a directory")
            return directory

        try:
            directory.mkdir(parents=True)
        except OSError as exc:
            raise RuntimeError(f"Could not create directory {directory}") from exc

        return directory

    def _get_formatter(self, formatter: Union[Type[Formatter], str, None]) -> Formatter:
        if formatter is None:
            return BUILTIN_FORMATTERS[DEFAULT_FORMATTER]()

        if isinstance(formatter, str):
            formatter_klass = BUILTIN_FORMATTERS.get(formatter.upper())
            if not formatter_klass:
                raise ValueError(f"Invalid formatter {formatter}")
            return formatter_klass()

        return formatter()

    def save(self, response: requests.Response) -> None:
        self.req_count += 1

        req_path = str(urlparse(response.request.url).path)

        if req_path == "/":
            req_info = "TODO"  # TODO
        else:
            req_info = f"{response.request.method}{req_path.replace('/', '_')}"

        req_fn = f"{self.req_count}_req__{req_info}.{self.formatter.file_extension}"
        resp_fn = f"{self.req_count}_resp__{req_info}.{self.formatter.file_extension}"

        Path(self.dir / resp_fn).write_text(self.formatter.export_response(response))
        Path(self.dir / req_fn).write_text(
            self.formatter.export_request(response.request),
        )
