"""工具."""
from .config import Config
from .logger import setup_logger
from .schema import (
    dump_instance,
    json,
    make_instance,
)

setup_logger()
__all__ = [
    "Config",
    "dump_instance",
    "json",
    "make_instance",
]
