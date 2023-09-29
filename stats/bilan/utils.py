import pandas as pd
import requests
import os
import json

from dotenv import load_dotenv


######################
# Variables globales
######################


CAMPAGNES = {
    "2021": {"start_date": "2022-07-16", "end_date": "2022-12-05", "card": "795"},
    "2022": {"start_date": "2023-02-13", "end_date": "2023-06-30", "card": "802"},
}

SECTORS = {
    "ESAT/établissements spécialisés": "social",
    "Secondaire lycée (hors agricole)": "education",
    "Restaurants inter-entreprises": "enterprise",
    "Restaurants d’entreprises": "enterprise",
    "Secondaire Lycée agricole": "education",
    "Restaurants inter-administratifs d’Etat (RIA)": "administration",
    "Cliniques": "health",
    "Autres établissements sociaux et médicaux sociaux": "social",
    "Restaurants des prisons": "administration",
    "Autres structures d’enseignement": "education",
    "Secondaire collège": "education",
    "Autres etablissements du secteur public": "administration",
    "Autres établissements de loisirs": "leisure",
    "Centre de vacances/sportif": "leisure",
    "Autres établissements de soins": "health",
    "Autres etablissements non listés": "autres",
    "Crèche": "social",
    "Ecole primaire (maternelle et élémentaire)": "education",
    "Restaurants des armées/police/gendarmerie": "administration",
    "Restaurants administratifs d’Etat (RA)": "administration",
    "EHPAD/ maisons de retraite / foyers de personnes âgées": "social",
    "Restaurants administratifs des collectivités territoriales": "administration",
    "IME/ITEP": "social",
    "Hôpitaux": "health",
    "Supérieur et Universitaire": "education",
}

APPRO_SIMPLIFIED = [
    "teledeclaration.value_bio_ht",
    "teledeclaration.value_total_ht",
    "teledeclaration.value_egalim_others_ht",
    "teledeclaration.value_sustainable_ht",
    "teledeclaration.value_externality_performance_ht",
]

COLUMNS_TO_SAVE = [
    "canteen.id",
    "applicant_id",
    "teledeclaration_mode",
    "creation_date",
    "status",
    "year",
    "diagnostic_id",
    "canteen.name",
    "canteen.siret",
    "canteen.city_insee_code",
    "applicant.name",
    "applicant.email",
    "satellites",
    "satellite_canteens_count",
    "canteen.region",
    "canteen.department",
    "central_kitchen_siret",
    "canteen.sectors",
    "canteen.line_ministry",
    "canteen.economic_model",
    "canteen.management_type",
    "canteen.production_type",
    "canteen.daily_meal_count",
    "canteen.yearly_meal_count",
    "canteen.central_producer_siret",
    "canteen.satellite_canteens_count",
    "teledeclaration.id",
    "teledeclaration.year",
    "teledeclaration.creation_date",
    "teledeclaration.value_bio_ht",
    "teledeclaration.value_total_ht",
    "teledeclaration.diagnostic_type",
    "teledeclaration.value_sustainable_ht",
    "teledeclaration.value_egalim_others_ht",
    "teledeclaration.value_externality_performance_ht",
]


######################
# Aggregation des TD complètes
######################


def aggregation_col(df, categ="bio", sub_categ=["_bio"]):
    pattern = "|".join(sub_categ)
    df[f"teledeclaration.value_{categ}_ht"] = df.filter(regex=pattern).sum(
        axis=1, numeric_only=True, skipna=True, min_count=1
    )
    return df


######################
# Extract
######################


def load_td():
    url = "https://ma-cantine-metabase.cleverapps.io/api/card/802/query/json"
    load_dotenv()

    if not os.environ.get("METABASE_TOKEN"):
        raise Exception("Pas de token Metabase trouvé")

    header = {
        "Content-Type": "application/json",
        "X-Metabase-Session": os.environ.get("METABASE_TOKEN"),
    }
    res = requests.post(
        url,
        headers=header,
    )
    if res.status_code != 200:
        raise Exception(f"Request failed : {res.status_code}")

    td_raw = pd.DataFrame(res.json())
    del td_raw["year"]
    td_raw["declared_data"] = td_raw["declared_data"].apply(json.loads)
    td_json = pd.json_normalize(td_raw["declared_data"])
    td_raw = pd.concat([td_raw.drop("declared_data", axis=1), td_json], axis=1)

    # Suppression des td sans information appros
    td_raw = td_raw.dropna(
        how="all",
        subset=APPRO_SIMPLIFIED,
    )
    td_raw = aggregation_col(td_raw, "bio", ["_bio"])
    td_raw = aggregation_col(td_raw, "sustainable", ["_sustainable", "_label_rouge", "_aocaop_igp_stg"])
    td_raw = aggregation_col(
        td_raw,
        "egalim_others",
        ["_egalim_others", "_hve", "_peche_durable", "_rup", "_fermier", "_commerce_equitable"],
    )
    td_raw = aggregation_col(
        td_raw, "externality_performance", ["_externality_performance", "_performance", "_externalites"]
    )
    return td_raw


def add_canteen_info(df):
    url = "https://ma-cantine-metabase.cleverapps.io/api/card/820/query/json"
    res = requests.post(
        url,
        headers={
            "Content-Type": "application/json",
            "X-Metabase-Session": os.environ.get("METABASE_TOKEN"),
        },
    )
    td_canteen = pd.DataFrame(res.json())
    col_to_rename = {}
    for col in ["production_type", "management_type", "yearly_meal_count", "daily_meal_count", "sectors"]:
        del df[f"canteen.{col}"]
        col_to_rename[f"{col}"] = f"canteen.{col}"
    td_canteen = td_canteen.rename(columns=col_to_rename)

    df = df.merge(right=td_canteen, left_on="canteen.id", right_on="id")
    return df


def split_td_into_years(td_raw):
    tds = {}
    td = td_raw.copy()
    td = td[td.status == "SUBMITTED"]
    for year in CAMPAGNES.keys():
        tds[year] = td.copy()
        tds[year] = tds[year][tds[year].year == int(year)]
        tds[year]["creation_date"] = tds[year]["creation_date"].apply(lambda x: x.split("T")[0])
        tds[year] = tds[year][
            (tds[year]["creation_date"] >= CAMPAGNES[year]["start_date"])
            & (tds[year]["creation_date"] <= CAMPAGNES[year]["end_date"])
        ]
    tds["2021"] = add_canteen_info(tds["2021"])
    return tds


######################
# Creation et affichage des indicateurs
######################


def calcul_indicateur(tds: {}, years=[], col_comparaison=True):
    return calcul_indicateur_divers(tds, years, col_comparaison), calcul_indicateur_appro(tds, years, col_comparaison)


def calcul_indicateur_divers(tds: {}, years=[], col_comparaison=True):
    indicateurs = {}
    for year in years if len(years) else tds.keys():
        indicateurs[year] = {}
        indicateurs[year]["Nombre de Télédéclarations"] = len(tds[year])
        indicateurs[year]["Nombre de sites de restauration concernés par la télédéclaration"] = (
            len(tds[year]) + tds[year]["satellite_canteens_count"].sum()
        )
        cuisines_sur_place = tds[year][tds[year]["canteen.production_type"].isin(["site", "site_cooked_elsewhere"])]
        indicateurs[year]["Nombre de cantines sur place (sites et satellites)"] = len(cuisines_sur_place)

        cuisines_centrales = tds[year][tds[year]["canteen.production_type"].isin(["central_serving", "central"])]
        indicateurs[year]["Nombre de cantines centrales"] = len(cuisines_centrales)

        indicateurs[year]["Nombre de repas moyens par jour pour les cantines sur place"] = int(
            cuisines_sur_place["canteen.daily_meal_count"].mean()
        )
        indicateurs[year]["Nombre de repas moyens par jour pour les cantines centrales"] = int(
            cuisines_centrales["canteen.daily_meal_count"].mean()
        )
        indicateurs[year]["Nombre de repas totaux pour l'année"] = int(tds[year]["canteen.yearly_meal_count"].sum())

        indicateurs[year]["Taux de cantines en gestion directe"] = len(
            tds[year][tds[year]["canteen.management_type"] == "direct"]
        ) / len(tds[year])
        indicateurs[year]["Taux de cantines en gestion concédée"] = len(
            tds[year][tds[year]["canteen.management_type"] == "conceded"]
        ) / len(tds[year])

        indicateurs[year]["Taux de TD simplifiées"] = len(
            tds[year][tds[year]["teledeclaration.diagnostic_type"] == "SIMPLE"]
        ) / len(tds[year])
    return pd.DataFrame(indicateurs)


def calcul_indicateur_appro(tds: {}, years=[], col_comparaison=True):
    indicateurs = {}
    for year in years if len(years) else tds.keys():
        indicateurs[year] = {}

        indicateurs[year]["Montant d'achat alimentaires"] = int(tds[year]["teledeclaration.value_total_ht"].sum())

        indicateurs[year]["Taux global des achats en bio"] = (
            tds[year]["teledeclaration.value_bio_ht"].sum() / tds[year]["teledeclaration.value_total_ht"].sum()
        )
        indicateurs[year]["Montant d'achat alimentaires bio"] = int(tds[year]["teledeclaration.value_bio_ht"].sum())

        indicateurs[year]["Taux global des achats EGALIM (bio inclus)"] = (
            tds[year]["teledeclaration.value_egalim_others_ht"].sum()
            + tds[year]["teledeclaration.value_externality_performance_ht"].sum()
            + tds[year]["teledeclaration.value_bio_ht"].sum()
            + tds[year]["teledeclaration.value_sustainable_ht"].sum()
        ) / tds[year]["teledeclaration.value_total_ht"].sum()

        indicateurs[year]["Montant d'achat alimentaires EGALIM (bio inclus)"] = (
            tds[year]["teledeclaration.value_egalim_others_ht"].sum()
            + tds[year]["teledeclaration.value_externality_performance_ht"].sum()
            + tds[year]["teledeclaration.value_bio_ht"].sum()
            + tds[year]["teledeclaration.value_sustainable_ht"].sum()
        )

        indicateurs[year]["Nombre de TD ayant déclaré 0€ d'achats en Bio"] = len(
            tds[year][tds[year]["teledeclaration.value_bio_ht"] == 0]
        )

    return pd.DataFrame(indicateurs)


def ajout_col_comparaison(indicateurs):
    if len(indicateurs.columns) != 2:
        print("Erreur : Il faut exactement 2 colonnes pour activer la comparaison")
    else:
        indicateurs["Comparaison"] = indicateurs[indicateurs.columns[1]] - indicateurs[indicateurs.columns[0]]
    return indicateurs


# Define custom formatter functions²
def nombre_formatter(value, comparaison=False):
    # Your custom formatting logic here
    return f"{value:,.0f}".replace(",", " ")


def taux_formatter(value):
    # Your custom formatting logic here
    return f"{100 * value:.2f} %"


def montant_formatter(value):
    # Your custom formatting logic here
    return f"{value:,.0f} €".replace(",", " ")


def display_indicateurs(df, transpose=True):
    if transpose:
        df = df.T
    df[df.columns[df.columns.str.startswith("Taux")]] = df[df.columns[df.columns.str.startswith("Taux")]].applymap(
        taux_formatter
    )
    df[df.columns[df.columns.str.startswith("Montant")]] = df[
        df.columns[df.columns.str.startswith("Montant")]
    ].applymap(montant_formatter)
    df[df.columns[df.columns.str.startswith("Nombre")]] = df[df.columns[df.columns.str.startswith("Nombre")]].applymap(
        nombre_formatter
    )
    if transpose:
        df = df.T
    if "Comparaison" in df.columns:
        df["Comparaison"] = df["Comparaison"].apply(lambda x: f"+{x}" if "-" not in x else x)
    print(df.to_html())


######################
# Divers
######################


def assert_quality(tds):
    for year in tds.keys():
        assert (
            tds[year].groupby("canteen.id").size().sort_values(ascending=False).head(1).iloc[0] == 1
        ), "Il y a des doublons de canteen.id"
        assert tds[year]["canteen.id"].isna().sum() == 0, "Il y a des cantines sans identifiant"
        assert len(tds[year]["canteen.id"]) == len(
            tds[year]["canteen.id"].unique()
        ), "Il y a des doublons dans les cantines"


def display_data_coverage(dfs, sub_columns=[], years=[]):
    """
    Takes a dict of DataFrame and display the coverage of data in a markdown table.
    If a subset of columns is given as an argument, only these columns will be take into account
    """
    pourcentage_in_file = {}
    for year in years if len(years) else dfs.keys():
        pourcentage_in_file[year] = {}
        for col in sub_columns if len(sub_columns) else dfs[year].columns:
            col_to_display = col.replace(".", " ").replace("_", " ")
            pourcentage_in_file[year][
                col_to_display
            ] = f"{100 * (1 - dfs[year][col].isna().sum() / len(dfs[year])):.2f} %"

    pourcentage_in_file_to_display = pd.DataFrame(pourcentage_in_file)
    pourcentage_in_file_to_display = pourcentage_in_file_to_display.rename(
        columns={"2022": "Part des valeurs renseignées (2022)", "2021": "Part des valeurs renseignées (2021)"}
    )
    print(pourcentage_in_file_to_display.to_html())
