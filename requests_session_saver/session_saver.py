from pathlib import Path
import tempfile
from typing import Type, Union

import requests

from .exporters import BUILTIN_EXPORTERS, Exporter

DEFAULT_EXPORTER = "JSON"


class SessionSaver:
    def __init__(
        self,
        session: requests.Session,  # TODO Intercept everything if no session?
        /,
        directory: Union[Path, None] = None,
        exporter: Union[Type[Exporter], str, None] = None,
    ) -> None:
        self.dir = self._get_work_dir(directory)
        self.exporter = self._get_exporter(exporter)

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

    def _get_exporter(self, exporter: Union[Type[Exporter], str, None]) -> Exporter:
        if exporter is None:
            return BUILTIN_EXPORTERS[DEFAULT_EXPORTER]()

        if isinstance(exporter, str):
            exporter_klass = BUILTIN_EXPORTERS.get(exporter.upper())
            if not exporter_klass:
                raise ValueError(f"Invalid exporter {exporter}")
            return exporter_klass()

        return exporter()

    def save(self, response: requests.Response) -> None:
        # TODO

        response_data = self.exporter.export_response(response)
        request_data = self.exporter.export_request(response.request)
