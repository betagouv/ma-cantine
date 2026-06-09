"""Compatibility imports for legacy canteen_managers_import view path."""

from backend.imports.canteen_managers import (
    CANTEEN_MANAGERS_SCHEMA_FILE_NAME,
    CANTEEN_MANAGERS_SCHEMA_FILE_PATH,
    CANTEEN_MANAGERS_SCHEMA_URL,
    CanteensManagersImportView,
    FileFormatError,
)

__all__ = [
    "CANTEEN_MANAGERS_SCHEMA_FILE_NAME",
    "CANTEEN_MANAGERS_SCHEMA_FILE_PATH",
    "CANTEEN_MANAGERS_SCHEMA_URL",
    "CanteensManagersImportView",
    "FileFormatError",
]
