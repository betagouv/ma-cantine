"""Compatibility imports for legacy purchase_import view path."""

from backend.imports.purchase import (
    PURCHASE_ID_SCHEMA_FILE_NAME,
    PURCHASE_ID_SCHEMA_FILE_PATH,
    PURCHASE_ID_SCHEMA_URL,
    PURCHASE_SIRET_SCHEMA_FILE_NAME,
    PURCHASE_SIRET_SCHEMA_FILE_PATH,
    PURCHASE_SIRET_SCHEMA_URL,
    PurchasesImportView,
)

__all__ = [
    "PURCHASE_ID_SCHEMA_FILE_NAME",
    "PURCHASE_ID_SCHEMA_FILE_PATH",
    "PURCHASE_ID_SCHEMA_URL",
    "PURCHASE_SIRET_SCHEMA_FILE_NAME",
    "PURCHASE_SIRET_SCHEMA_FILE_PATH",
    "PURCHASE_SIRET_SCHEMA_URL",
    "PurchasesImportView",
]
