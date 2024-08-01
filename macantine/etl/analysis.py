import pandas as pd
import logging
import json
import numpy as np

from macantine.etl.data_warehouse import DataWareHouse
from macantine.etl import etl

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
        return "B) oui"
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
    return (
        row["teledeclaration.value_externality_performance_ht"]
        + row["teledeclaration.value_sustainable_ht"]
        + row["teledeclaration.value_egalim_others_ht"]
    )


def get_egalim_avec_bio(row):
    return (
        row["teledeclaration.value_bio_ht"]
        + row["teledeclaration.value_externality_performance_ht"]
        + row["teledeclaration.value_sustainable_ht"]
        + row["teledeclaration.value_egalim_others_ht"]
    )


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
        else:
            return "Autre"


def get_ratio_egalim_fish(row):
    if row["teledeclaration.value_fish_ht"] > 0 and row["teledeclaration.value_fish_egalim_ht"] >= 0:
        return 100 * row["teledeclaration.value_fish_egalim_ht"] / row["teledeclaration.value_fish_ht"]
    else:
        return np.nan


def get_ratio_egalim_meat_poultry(row):
    if row["teledeclaration.value_meat_poultry_ht"] > 0 and row["teledeclaration.value_meat_poultry_egalim_ht"] >= 0:
        return 100 * row["teledeclaration.value_meat_poultry_egalim_ht"] / row["teledeclaration.value_meat_poultry_ht"]
    else:
        return np.nan


def get_ratio_bio(row):
    if row["teledeclaration.value_total_ht"] > 0 and row["teledeclaration.value_bio_ht"] >= 0:
        return 100 * row["teledeclaration.value_bio_ht"] / row["teledeclaration.value_total_ht"]
    else:
        return np.nan


def get_ratio_egalim_avec_bio(row):
    if row["teledeclaration.value_total_ht"] > 0 and row["teledeclaration.value_somme_egalim_avec_bio_ht"] >= 0:
        return 100 * row["teledeclaration.value_somme_egalim_avec_bio_ht"] / row["teledeclaration.value_total_ht"]
    else:
        return np.nan


def get_ratio_egalim_sans_bio(row):
    if row["teledeclaration.value_total_ht"] > 0 and row["teledeclaration.value_somme_egalim_hors_bio_ht"] >= 0:
        return 100 * row["teledeclaration.value_somme_egalim_hors_bio_ht"] / row["teledeclaration.value_total_ht"]
    else:
        return np.nan


def transform_sector_column(row):
    """
    Fetching sectors information and aggreting in list in order to have only one row per canteen
    """
    if type(row) == list:
        if len(row) > 1:
            return pd.Series({"secteur": "Secteurs multiples", "catégorie": "Catégories multiples"})
        elif len(row) == 1:
            return pd.Series({"secteur": row[0]["name"], "catégorie": row[0]["category"]})
    return pd.Series({"secteur": np.nan, "catégorie": np.nan})


def aggregate_col(df, categ="bio", sub_categ=["_bio"]):
    pattern = "|".join(sub_categ)
    df[f"teledeclaration.value_{categ}_ht"] = df.filter(regex=pattern).sum(
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
    df = aggregate_col(df, "externality_performance", ["_externality_performance", "_performance", "_externalites"])
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
        self.years = etl.CAMPAIGN_DATES.keys()
        self.extracted_table_name = "teledeclarations_extracted"
        self.warehouse = DataWareHouse()
        self.schema = json.load(open("data/schemas/schema_analysis.json"))

    def extract_dataset(self):
        # Load teledeclarations from prod database into the Data Warehouse
        self.df = etl.fetch_teledeclarations(self.years)

    def transform_dataset(self):
        # Flatten json 'declared_data' column
        df_json = pd.json_normalize(self.df["declared_data"])
        del df_json["year"]
        self.df = self.df.loc[~self.df.index.duplicated(keep="first")]
        self.df = pd.concat([self.df.drop("declared_data", axis=1), df_json], axis=1)

        # Calculate columns
        self.df["management_type"] = self.df["canteen.management_type"].apply(get_management_type)
        self.df["cuisine_centrale"] = self.df["canteen.production_type"].apply(get_management_type)
        self.df["modele_economique"] = self.df["canteen.economic_model"].apply(get_economic_model)
        self.df["diagnostic_type"] = self.df["teledeclaration.diagnostic_type"].apply(get_economic_model)
        self.df["nbre_cantines_region"] = self.df["canteen.region"].apply(get_nbre_cantines_region)
        self.df["objectif_zone_geo"] = self.df["canteen.region"].apply(get_objectif_zone_geo)
        self.df["teledeclaration.value_somme_egalim_avec_bio_ht"] = self.df.apply(get_egalim_avec_bio, axis=1)
        self.df["teledeclaration.value_somme_egalim_hors_bio_ht"] = self.df.apply(get_egalim_hors_bio, axis=1)
        self.df["teledeclaration.value_meat_and_fish_ht"] = self.df.apply(get_meat_and_fish, axis=1)
        self.df["teledeclaration.value_meat_and_fish_egalim_ht"] = self.df.apply(get_meat_and_fish_egalim, axis=1)

        self.df["ratio_egalim_fish"] = self.df.apply(get_ratio_egalim_fish, axis=1)
        self.df["ratio_egalim_meat_poultry"] = self.df.apply(get_ratio_egalim_meat_poultry, axis=1)
        self.df["ratio_bio"] = self.df.apply(get_ratio_bio, axis=1)
        self.df["ratio_egalim_avec_bio"] = self.df.apply(get_ratio_egalim_avec_bio, axis=1)
        self.df["ratio_egalim_sans_bio"] = self.df.apply(get_ratio_egalim_sans_bio, axis=1)

        # Convert types
        self.df["daily_meal_count"] = pd.to_numeric(self.df["canteen.daily_meal_count"], errors="coerce")
        self.df["yearly_meal_count"] = pd.to_numeric(self.df["canteen.yearly_meal_count"], errors="coerce")
        self.df["satellite_canteens_count"] = pd.to_numeric(
            self.df["canteen.satellite_canteens_count"], errors="coerce"
        )

        # Fill geo data
        for geo in ["department", "region"]:
            geo = f"canteen.{geo}"
            logger.info("Start filling geo_name")
            self.fill_geo_names(geo_zoom=geo)
            col_geo = self.df.pop(f"{geo}_lib")
            self.df.insert(self.df.columns.get_loc(geo) + 1, f"{geo}_lib", col_geo)

        # Fill campaign participation
        logger.info("Canteens : Fill campaign participations...")
        for year in etl.CAMPAIGN_DATES.keys():
            campaign_participation = etl.map_canteens_td(year)
            col_name_campaign = f"declaration_{year}"
            self.df[col_name_campaign] = self.df["id"].apply(lambda x: x in campaign_participation)

        # Extract the sector names and categories
        logger.info("Canteens : Extract sectors...")
        self.df[["secteur", "catégorie"]] = self.df["canteen.sectors"].apply(
            lambda x: (
                transform_sector_column(x) if x != np.nan else pd.Series({"secteur": np.nan, "catégorie": np.nan})
            )
        )

        # Aggregate columns for complete TD
        self.df = aggregate(self.df)

        # Rename columns
        self.df = self.df.rename(
            columns={
                "teledeclaration.id": "id",
                "canteen.id": "canteen_id",
                "applicant.id": "applicant_id",
                "diagnostic_id": "diagnostic_id",
                "canteen.region_lib": "canteen.lib_region",
                "canteen.department_lib": "canteen.lib_department",
            }
        )
        self.df.columns = self.df.columns.str.replace("teledeclaration.", "")
        self.df.columns = self.df.columns.str.replace("canteen.", "")
        self.df.columns = self.df.columns.str.replace("applicant.", "")
        self.df.columns = self.df.columns.str.replace("department", "departement")

        # Filter by schema columns names
        columns = [i["name"] for i in self.schema["fields"]]
        self.df = self.df[columns]

    def load_dataset(self):
        """
        Load in database
        """
        # For testing
        self.warehouse.insert_dataframe(self.df, self.extracted_table_name)
