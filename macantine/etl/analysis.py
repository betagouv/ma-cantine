import json
import logging
import re

import numpy as np
import pandas as pd

from macantine.etl import etl, utils
from macantine.etl.data_ware_house import DataWareHouse

logger = logging.getLogger(__name__)

# Source : query Resytal dec 2023
ESTIMATED_NUMBER_CANTEENS_REGION = {
    1: 625,
    2: 554,
    3: 161,
    4: 900,
    6: 203,
    11: 13235,
    24: 4171,
    27: 3623,
    28: 4360,
    32: 7061,
    44: 7324,
    52: 4545,
    53: 4279,
    75: 8854,
    76: 7336,
    84: 10842,
    93: 5991,
    94: 395,
}


def get_management_type(value):
    if value == "direct":
        return "A) directe"
    elif value == "conceded":
        return "B) concédée"
    else:
        return "C) non renseigné"


def get_cuisine_centrale(value):
    if value in ["site", "site_cooked_elsewhere"]:
        return "B) non"
    elif value in ["central", "central_serving"]:
        return "A) oui"
    else:
        return "C) non renseigné"


def get_economic_model(value):
    if value == "private":
        return "A) privé"
    elif value == "public":
        return "B) public"
    else:
        return "C) non renseigné"


def get_diagnostic_type(value):
    if value == "COMPLETE":
        return "A) détaillée"
    elif value == "SIMPLE":
        return "B) simple"
    else:
        return "C) non renseigné"


def get_egalim_hors_bio(row):
    """
    Aggregating egalim values.
    Processing of empty values : As decided for analysis, if there are empty values, we convert them to zeros
    in order to avoid losing too many lines (this doesn't apply to value_bio_ht and value_total_ht, for which we filter out the empty values)
    """
    egalim_hors_bio = 0
    for categ in ["externality_performance", "sustainable", "egalim_others"]:
        value_categ = row[f"teledeclaration.value_{categ}_ht"] if row[f"teledeclaration.value_{categ}_ht"] >= 0 else 0
        egalim_hors_bio += value_categ
    return egalim_hors_bio


def get_egalim_avec_bio(row):
    return row["teledeclaration.value_bio_ht"] + get_egalim_hors_bio(row)


def get_meat_and_fish(row):
    return row["teledeclaration.value_meat_poultry_ht"] + row["teledeclaration.value_fish_ht"]


def get_meat_and_fish_egalim(row):
    return row["teledeclaration.value_meat_poultry_egalim_ht"] + row["teledeclaration.value_fish_egalim_ht"]


def get_nbre_cantines_region(region: int):
    if region in ESTIMATED_NUMBER_CANTEENS_REGION.keys():
        return ESTIMATED_NUMBER_CANTEENS_REGION[region]
    else:
        return np.nan


def get_objectif_zone_geo(department: int):
    if department and department != "nan" and not pd.isna(department):
        # Dealing with two string codes
        if department == "2A" or department == "2B":
            return "France métropolitaine"
        department = int(department)
        if department >= 1 and department <= 95:
            return "France métropolitaine"
        elif department == 976:
            return "DROM (Mayotte)"
        elif department >= 971 and department <= 978:
            return "DROM (hors Mayotte)"
    return "non renseigné"


def get_ratio_egalim_fish(row):
    return utils.get_ratio(row, "value_fish_egalim_ht", "value_fish_ht")


def get_ratio_egalim_meat_poultry(row):
    return utils.get_ratio(row, "value_meat_poultry_egalim_ht", "value_meat_poultry_ht")


def get_ratio_bio(row):
    return utils.get_ratio(row, "value_bio_ht", "value_total_ht")


def get_ratio_egalim_avec_bio(row):
    return utils.get_ratio(row, "value_somme_egalim_avec_bio_ht", "value_total_ht")


def get_ratio_egalim_sans_bio(row):
    return utils.get_ratio(row, "value_somme_egalim_hors_bio_ht", "value_total_ht")


def format_sector_column(row: pd.Series, sector_col_name: str):
    """
    Splitting sectors information into two new columns, one for the sector, one for the category
    If there are multiple sectors, we
    """
    x = row[sector_col_name]
    if type(x) == list:
        if len(x) > 1:
            return "Secteurs multiples", "Catégories multiples"
        elif len(x) == 1:
            return x[0]["name"], x[0]["category"]
    return np.nan, np.nan


def check_column_matches_substring(df, sub_categ: str):
    for substring in sub_categ:
        pattern = rf".*{re.escape(substring)}.*"
        matching_cols = df.filter(regex=pattern).columns.tolist()
        if len(matching_cols) == 0:
            logger.error("The sub categ {substring} doesn't match any columns from the dataframe")
            raise KeyError


def aggregate_col(df, categ, sub_categ):
    """
    Aggregating into a new column all the values of a category for complete TD
    """
    check_column_matches_substring(df, sub_categ)
    regex_pattern = rf"^(?!value_{categ}_ht$).*(" + "|".join(sub_categ) + ")"
    df[f"teledeclaration.value_{categ}_ht"] = df.filter(regex=regex_pattern).sum(
        axis=1, numeric_only=True, skipna=True, min_count=1
    )
    return df


def aggregate(df):
    df = aggregate_col(df, "bio", ["_bio"])
    df = aggregate_col(df, "sustainable", ["_sustainable", "_label_rouge", "_aocaop_igp_stg"])
    df = aggregate_col(
        df,
        "egalim_others",
        ["_egalim_others", "_hve", "_peche_durable", "_rup", "_fermier", "_commerce_equitable"],
    )
    df = aggregate_col(df, "externality_performance", ["_performance", "_externalites"])
    df["teledeclaration.cout_denrees"] = df.apply(
        lambda row: row["teledeclaration.value_total_ht"] / row["canteen.yearly_meal_count"], axis=1
    )
    return df


class ETL_ANALYSIS(etl.ETL):
    """
    Create a dataset for analysis in a Data Warehouse
    * Extract data from prod
    * Run a SQL query using Metabase API to transform the dataset
    * Load the transformed data in a new table within the Data WareHouse
    """

    def __init__(self):
        self.df = None
        self.extracted_table_name = ""
        self.schema = ""
        self.warehouse = DataWareHouse()

    def load_dataset(self):
        """
        Load in database
        """
        self.warehouse.insert_dataframe(self.df, self.extracted_table_name)


class ETL_ANALYSIS_TD(ETL_ANALYSIS):
    """
    Create a dataset for analysis in a Data Warehouse
    * Extract data from prod
    * Run a SQL query using Metabase API to transform the dataset
    * Load the transformed data in a new table within the Data WareHouse
    """

    def __init__(self):
        self.df = None
        self.years = utils.CAMPAIGN_DATES.keys()
        self.extracted_table_name = "teledeclarations_extracted"
        self.warehouse = DataWareHouse()
        self.schema = json.load(open("data/schemas/schema_analysis.json"))

    def extract_dataset(self):
        # Load teledeclarations from prod database into the Data Warehouse
        self.df = utils.fetch_teledeclarations(self.years)
        self.df.index = self.df.id

    def transform_dataset(self):
        # Flatten json 'declared_data' column
        df_json = pd.json_normalize(self.df["declared_data"])
        del df_json["year"]
        del df_json["canteen.id"]
        df_json.index = self.df.id
        self.df = self.df.loc[~self.df.index.duplicated(keep="first")]
        self.df = pd.concat([self.df.drop("declared_data", axis=1), df_json], axis=1)

        # Aggregate columns for complete TD - Must occur before other transformations
        self.df = aggregate(self.df)

        self.compute_miscellaneous_columns()

        # Convert types
        self.df["daily_meal_count"] = pd.to_numeric(self.df["canteen.daily_meal_count"], errors="coerce")
        self.df["yearly_meal_count"] = pd.to_numeric(self.df["canteen.yearly_meal_count"], errors="coerce")
        self.df["satellite_canteens_count"] = pd.to_numeric(
            self.df["canteen.satellite_canteens_count"], errors="coerce"
        )

        logger.info("Start filling geo_name")
        self.fill_geo_names(prefix="canteen.")

        # Fill campaign participation
        logger.info("Canteens : Fill campaign participations...")
        for year in utils.CAMPAIGN_DATES.keys():
            campaign_participation = utils.map_canteens_td(year)
            col_name_campaign = f"declaration_{year}"
            self.df[col_name_campaign] = self.df["id"].apply(lambda x: x in campaign_participation)

        # Extract the sector names and categories
        logger.info("Canteens : Extract sectors...")
        self.df[["secteur", "catégorie"]] = self.df["canteen.sectors"].apply(
            lambda x: format_sector_column(x, "canteen.sectors"), axis=1, result_type="expand"
        )

        # Rename columns
        self.df = self.df.rename(
            columns={
                "teledeclaration.id": "id",
                "diagnostic_id": "diagnostic_id",
                "canteen.region_lib": "canteen.lib_region",
                "canteen.department_lib": "canteen.lib_department",
            }
        )
        self.df.columns = self.df.columns.str.replace("teledeclaration.", "")
        self.df.columns = self.df.columns.str.replace("canteen.", "")
        self.df.columns = self.df.columns.str.replace("applicant.", "")
        self.df.columns = self.df.columns.str.replace("department", "departement")

        self.df = utils.filter_dataframe_with_schema_cols(self.df, self.schema)

    def compute_miscellaneous_columns(self):
        # Canteen
        self.df["management_type"] = self.df["canteen.management_type"].apply(get_management_type)
        self.df["cuisine_centrale"] = self.df["canteen.production_type"].apply(get_cuisine_centrale)
        self.df["modele_economique"] = self.df["canteen.economic_model"].apply(get_economic_model)
        self.df["diagnostic_type"] = self.df["teledeclaration.diagnostic_type"].apply(get_diagnostic_type)
        # Add geo data
        self.df["nbre_cantines_region"] = self.df["canteen.region"].apply(get_nbre_cantines_region)
        self.df["objectif_zone_geo"] = self.df["canteen.region"].apply(get_objectif_zone_geo)
        # Combine columns
        self.df["teledeclaration.value_somme_egalim_avec_bio_ht"] = self.df.apply(get_egalim_avec_bio, axis=1)
        self.df["teledeclaration.value_somme_egalim_hors_bio_ht"] = self.df.apply(get_egalim_hors_bio, axis=1)
        self.df["teledeclaration.value_meat_and_fish_ht"] = self.df.apply(get_meat_and_fish, axis=1)
        self.df["teledeclaration.value_meat_and_fish_egalim_ht"] = self.df.apply(get_meat_and_fish_egalim, axis=1)
        # Calcul ratio
        self.df["ratio_egalim_fish"] = self.df.apply(get_ratio_egalim_fish, axis=1)
        self.df["ratio_egalim_meat_poultry"] = self.df.apply(get_ratio_egalim_meat_poultry, axis=1)
        self.df["ratio_bio"] = self.df.apply(get_ratio_bio, axis=1)
        self.df["ratio_egalim_avec_bio"] = self.df.apply(get_ratio_egalim_avec_bio, axis=1)
        self.df["ratio_egalim_sans_bio"] = self.df.apply(get_ratio_egalim_sans_bio, axis=1)


class ETL_ANALYSIS_CANTEEN(ETL_ANALYSIS):
    """
    Create a dataset for analysis in a Data Warehouse
    * Extract data from prod
    * Run a SQL query using Metabase API to transform the dataset
    * Load the transformed data in a new table within the Data WareHouse

    How to add a new field ? Add it to the corresponding schema : schema_analysis_cantines.json
    - If it's a extracted field : Add it to the columns_mapper with its translation
    - If it's a generated field : Add it in the transform_dataset()
    """

    def __init__(self):
        self.df = None
        self.extracted_table_name = "canteens_extracted"
        self.warehouse = DataWareHouse()
        self.schema = json.load(open("data/schemas/schema_analysis_cantines.json"))
        # The following mapper is used for renaming columns and for selecting the columns to extract from db
        self.columns_mapper = {
            "id": "id",
            "name": "nom",
            "siret": "siret",
            "city_insee_code": "code_insee_commune",
            "city": "libelle_commune",
            "department": "departement",
            "region": "region",
            "creation_date": "date_creation",
            "modification_date": "date_modification",
            "daily_meal_count": "nbre_repas_jour",
            "yearly_meal_count": "nbre_repas_an",
            "economic_model": "modele_economique",
            "management_type": "type_gestion",
            "production_type": "type_production",
            "satellite_canteens_count": "nombre_satellites",
            "central_producer_siret": "siret_cuisine_centrale",
        }

    def extract_dataset(self):
        self.df = utils.fetch_canteens(self.columns_mapper.keys())

    def transform_dataset(self):

        logger.info("Filling geo names")
        self.fill_geo_names()
        self.columns_mapper["department_lib"] = "departement_lib"

        self.df = self.df.rename(columns=self.columns_mapper)
        self.df = utils.filter_dataframe_with_schema_cols(self.df, self.schema)
