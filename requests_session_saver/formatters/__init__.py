from typing import Dict, Type

from requests_session_saver.formatters.formatter import Formatter
from requests_session_saver.formatters.json import JsonFormatter
from requests_session_saver.formatters.raw import RawFormatter

BUILTIN_FORMATTERS: Dict[str, Type[Formatter]] = {
    "RAW": RawFormatter,
    "JSON": JsonFormatter,
}

__all__ = (
    "BUILTIN_FORMATTERS",
    "Exporter",
    "JsonExporter",
    "RawExporter",
)
