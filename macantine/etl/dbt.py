"""
DBT ETL Module

This module provides ETL classes to extract data from Django models and load them
into the Data Warehouse for use with DBT (Data Build Tool).

Usage:
    # Extract and load Canteens
    etl_canteens = ETL_DBT_CANTEENS()
    etl_canteens.extract_dataset()
    etl_canteens.transform_dataset()
    etl_canteens.load_dataset()

    # Extract and load Diagnostics
    etl_diagnostics = ETL_DBT_DIAGNOSTICS()
    etl_diagnostics.extract_dataset()
    etl_diagnostics.transform_dataset()
    etl_diagnostics.load_dataset()

    # Extract and load Purchases
    etl_purchases = ETL_DBT_PURCHASES()
    etl_purchases.extract_dataset()
    etl_purchases.transform_dataset()
    etl_purchases.load_dataset()

The data will be loaded into tables named:
- canteens
- diagnostics
- purchases

in the Data Warehouse configured via environment variables:
- DATA_WARE_HOUSE_USER
- DATA_WARE_HOUSE_PASSWORD
- DATA_WARE_HOUSE_HOST
- DATA_WARE_HOUSE_PORT
- DATA_WARE_HOUSE_DB
"""

import logging

from rest_framework.generics import ListAPIView

from api.serializers import PurchaseSerializer
from api.views.canteen import CanteenAnalysisListView
from api.views.diagnostic_teledeclaration import DiagnosticTeledeclaredAnalysisListView
from data.models import Purchase
from macantine.etl import etl
from macantine.etl.data_ware_house import DataWareHouse

logger = logging.getLogger(__name__)


class DBT(etl.TRANSFORMER_LOADER):
    """
    Base class for DBT (Data Build Tool) ETL process
    Extract data from Django models and load into Data Warehouse
    Minimal transformation - DBT handles most transformations
    """

    def __init__(self):
        super().__init__()
        self.extracted_table_name = ""
        self.warehouse = DataWareHouse()

    def transform_dataset(self):
        """
        Minimal transformation for DBT - most transformation happens in DBT itself
        """
        if self.df.empty:
            logger.warning(f"Dataset {self.extracted_table_name} is empty. Skipping transformation")
            return

        logger.info(f"Transforming {len(self.df)} rows for {self.extracted_table_name}")

    def load_dataset(self):
        """
        Load data into Data Warehouse
        """
        if self.df.empty:
            logger.warning(f"Dataset {self.extracted_table_name} is empty. Skipping load")
            return

        logger.info(f"Loading {len(self.df)} objects into Data Warehouse table: {self.extracted_table_name}")
        self.warehouse.insert_dataframe(self.df, self.extracted_table_name)
        logger.info(f"Successfully loaded {len(self.df)} rows into {self.extracted_table_name}")


class PurchaseAnalysisListView(ListAPIView):
    """
    View for DBT export - returns all purchases
    """

    serializer_class = PurchaseSerializer

    def get_queryset(self):
        return Purchase.objects.select_related("canteen").order_by("creation_date")


# ETL Classes
class ETL_DBT_CANTEENS(etl.EXTRACTOR, DBT):
    """
    Extract all Canteens from prod database and load into Data Warehouse
    """

    def __init__(self):
        super().__init__()
        self.extracted_table_name = "canteens"
        self.view = CanteenAnalysisListView


class ETL_DBT_DIAGNOSTICS(etl.EXTRACTOR, DBT):
    """
    Extract all Diagnostics from prod database and load into Data Warehouse
    """

    def __init__(self):
        super().__init__()
        self.extracted_table_name = "diagnostics"
        self.view = DiagnosticTeledeclaredAnalysisListView


class ETL_DBT_PURCHASES(etl.EXTRACTOR, DBT):
    """
    Extract all Purchases from prod database and load into Data Warehouse
    """

    def __init__(self):
        super().__init__()
        self.extracted_table_name = "purchases"
        self.view = PurchaseAnalysisListView
