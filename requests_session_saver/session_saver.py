from pathlib import Path
import tempfile
from typing import Tuple, Type, Union
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

    def _get_file_name(self, request: requests.PreparedRequest) -> Tuple[str, str]:
        req_path = str(urlparse(request.url).path)

        req_info = f"{request.method}_{req_path.replace('/', '_')}"
        ext = getattr(self.formatter, "file_extension", "")
        if ext:
            ext = "." + ext

        return (
            f"{self.req_count}_req__{req_info}{ext}",
            f"{self.req_count}_resp__{req_info}.{ext}",
        )

    def save(self, response: requests.Response) -> None:
        self.req_count += 1

        req_fpath, resp_fpath = self._get_file_name(response.request)

        Path(self.dir / req_fpath).write_text(
            self.formatter.format_request(response.request),
        )
        Path(self.dir / resp_fpath).write_text(self.formatter.format_response(response))
