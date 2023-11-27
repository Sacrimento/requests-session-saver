from typing import Dict, Type

from requests_session_saver.exporters.exporter import Exporter
from requests_session_saver.exporters.json import JsonExporter
from requests_session_saver.exporters.raw import RawExporter

BUILTIN_EXPORTERS: Dict[str, Type[Exporter]] = {
    "RAW": RawExporter,
    "JSON": JsonExporter,
}

__all__ = (
    "BUILTIN_EXPORTERS",
    "Exporter",
    "JsonExporter",
    "RawExporter",
)
