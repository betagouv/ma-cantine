import logging
import tempfile
import time

from django.contrib.postgres.fields import ArrayField
from django.db import connection

from macantine.etl import etl
from macantine.etl.data_ware_house import DataWareHouse, get_column_types

logger = logging.getLogger(__name__)


class ETL_ANALYSIS_RAW(etl.TRANSFORMER_LOADER):
    """
    Copy a table as-is to the analysis Data Warehouse (used as a dbt source).
    * Extract: Postgres COPY of the queryset rows into a temporary file on disk (no pandas)
    * Load: Postgres COPY of the file into the Data Warehouse table (see DataWareHouse.copy_file)

    Column types are the ones of the source table, except arrays which are converted to jsonb.
    Columns listed in exclude_columns are not exported (e.g. sensitive data).
    """

    def __init__(self, dataset_name, queryset, exclude_columns=None):
        super().__init__()
        self.warehouse = DataWareHouse()
        self.dataset_name = dataset_name
        self.queryset = queryset
        self.exclude_columns = exclude_columns or []
        self.column_types = {}
        self.file = None

    def extract_dataset(self):
        start = time.time()
        model = self.queryset.model
        unknown_columns = set(self.exclude_columns) - {field.column for field in model._meta.concrete_fields}
        if unknown_columns:
            # fail instead of silently exporting a column because of a typo
            raise ValueError(
                f"Unknown columns to exclude from {self.dataset_name}: {', '.join(sorted(unknown_columns))}"
            )
        fields = [field for field in model._meta.concrete_fields if field.column not in self.exclude_columns]

        sql, params = self.queryset.order_by().values(*[field.attname for field in fields]).query.sql_with_params()
        select = ", ".join(
            f'to_jsonb("{field.column}") AS "{field.column}"' if isinstance(field, ArrayField) else f'"{field.column}"'
            for field in fields
        )

        self.file = tempfile.TemporaryFile()
        with connection.cursor() as cursor:
            source_column_types = get_column_types(cursor, model._meta.db_table)
            copy_sql = cursor.mogrify(f"COPY (SELECT {select} FROM ({sql}) AS source) TO STDOUT", params).decode()
            cursor.copy_expert(copy_sql, self.file)
        self.column_types = {
            field.column: "jsonb" if isinstance(field, ArrayField) else source_column_types[field.column]
            for field in fields
        }

        end = time.time()
        logger.info(
            f"Time spent on {self.dataset_name} extraction: {end - start:.2f} seconds ({self.file.tell() / 1024 / 1024:.1f} MB)"
        )

    def transform_dataset(self):
        pass

    def load_dataset(self):
        try:
            self.file.seek(0)
            self.warehouse.copy_file(self.file, self.dataset_name, self.column_types)
        finally:
            self.file.close()
