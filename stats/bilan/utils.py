import pandas as pd
import requests
import os
import json

from unidecode import unidecode
from dotenv import load_dotenv


import geoviews as gv
import geoviews.feature as gf
import xarray as xr
from cartopy import crs
import numpy as np
import geopandas as gpd
from geoviews import dim

gv.extension("bokeh")


######################
# Variables globales
######################


CAMPAGNES = {
    "2022": {"start_date": "2022-07-16", "end_date": "2022-12-05", "card": "795"},
    "2023": {"start_date": "2023-02-13", "end_date": "2023-06-30", "card": "802"},
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
    "Secteurs multiples": "multiple_sectors",
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
    "teledeclaration.value_meat_poultry_egalim_ht",
    "teledeclaration.value_meat_poultry_ht",
    "teledeclaration.value_meat_poultry_france_ht",
    "teledeclaration.value_fish_ht",
    "teledeclaration.value_fish_egalim_ht",
    # "teledeclaration.cout_denrees",
]

TUNNEL_DATA_ENG = {}


def mapper_sector_diff(sector):
    sector = sector.replace("IME / ITEP", "IME/ITEP")
    sector = sector.replace(
        "EHPAD / maisons de retraite / foyers de personnes âgées",
        "EHPAD/ maisons de retraite / foyers de personnes âgées",
    )
    sector = sector.replace("ESAT / Etablissements spécialisés", "ESAT/établissements spécialisés")
    sector = sector.replace(
        "Restaurants des armées / police / gendarmerie", "Restaurants des armées/police/gendarmerie"
    )
    return sector

######################
# Aggregation des TD complètes
######################


def aggregation_col(df, categ="bio", sub_categ=["_bio"]):
    pattern = "|".join(sub_categ)
    df[f"teledeclaration.value_{categ}_ht"] = df.filter(regex=pattern).sum(
        axis=1, numeric_only=True, skipna=True, min_count=1
    )
    return df


def normalize_sector(secteur):
    return unidecode(secteur.lower())


######################
# Extract
######################


def clean_td(td, year):
    # Suppression de valeurs extremes
    mask = (td['canteen.id'] == 6724) | (td['canteen.id'] == 69589)
    td = td[~mask]

    # Save file status
    TUNNEL_DATA_ENG[year]['Après suppression TD aberrantes'] = len(td)
    return td


def transform_td(td_raw, year):
    """
    Transformation du jeu de données de télédéclarations
    Les traitements sur les dates sont fait plus tard
    """
    # Suppression des diagnostics non soumis
    td = td_raw[td_raw.status == "SUBMITTED"]

    # Save file status
    TUNNEL_DATA_ENG[year]['Après suppression des TD annulées'] = len(td)

    # Keeping only the columns we want
    td = td[COLUMNS_TO_SAVE]
    # Suppression des td sans information appros
    td = td.copy().dropna(
        how="all",
        subset=APPRO_SIMPLIFIED,
    )

    # Save file status
    TUNNEL_DATA_ENG[year]['Après suppression des TD sans données appro'] = len(td)

    # Fill na for canteen.yearly_meal_count in order to compute "cout denrees"
    td['canteen.yearly_meal_count'] = td['canteen.yearly_meal_count'].fillna(-1).replace(0, -1)
    td = clean_td(td, year)
    return td


def add_canteen_info(df, add_carac=True, add_geo=True):
    url = "https://ma-cantine-metabase.cleverapps.io/api/card/820/query/json"
    res = requests.post(
        url,
        headers={
            "Content-Type": "application/json",
            "X-Metabase-Session": os.environ.get("METABASE_TOKEN"),
        },
    )
    td_canteen = pd.DataFrame(res.json())

    col_to_merge = []
    if add_carac:
        col_to_merge = col_to_merge + [
            "production_type",
            "management_type",
            "yearly_meal_count",
            "daily_meal_count",
            "sectors",
        ]
    if add_geo:
        col_to_merge = col_to_merge + ["region", "department", "city_insee_code"]

    for col in col_to_merge:
        del df[f"canteen.{col}"]
    td_canteen = td_canteen.add_prefix("canteen.")
    col_to_merge = ["canteen." + sub for sub in col_to_merge]
    df = df.merge(right=td_canteen[col_to_merge + ["canteen.id"]], on="canteen.id")
    return df


def split_td_into_years(td_raw):
    tds = {}
    td = td_raw.copy()
    for year in CAMPAGNES.keys():
        tds[year] = td.copy()
        tds[year]["year"] = tds[year]["year"].apply(lambda x: x + 1)
        tds[year] = tds[year][tds[year].year == int(year)]
        tds[year]["creation_date"] = tds[year]["creation_date"].apply(lambda x: x.split("T")[0])
        tds[year] = tds[year][
            (tds[year]["creation_date"] >= CAMPAGNES[year]["start_date"])
            & (tds[year]["creation_date"] <= CAMPAGNES[year]["end_date"])
        ]
    tds["2022"] = add_canteen_info(tds["2022"], add_carac=True, add_geo=True)
    tds["2023"] = add_canteen_info(tds["2023"], add_carac=False, add_geo=True)
    return tds


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
    
    # Deleting line terminator substring that could corrupt the file
    td_raw['teledeclaration.other_waste_comments'] = td_raw['teledeclaration.other_waste_comments'].replace('\r\n', ' ', regex=True).replace('\n', ' ', regex=True)
    
    tds = split_td_into_years(td_raw)
    
    for year in CAMPAGNES.keys():
        TUNNEL_DATA_ENG[year] = {}
        # Save raw file (all years, all status, all columns)
        tds[year].to_csv(f"data/export_dataset_stats_campagne_raw_{year}.csv", sep=";", index=False)
        
        # Save file status
        TUNNEL_DATA_ENG[year]['Fichier brut'] = len(tds[year])

        tds[year] = aggregation_col(tds[year], "bio", ["_bio"])
        tds[year] = aggregation_col(tds[year], "sustainable", ["_sustainable", "_label_rouge", "_aocaop_igp_stg"])
        tds[year] = aggregation_col(
            tds[year],
            "egalim_others",
            ["_egalim_others", "_hve", "_peche_durable", "_rup", "_fermier", "_commerce_equitable"],
        )
        tds[year] = aggregation_col(
            tds[year], "externality_performance", ["_externality_performance", "_performance", "_externalites"]
        )

        tds[year] = transform_td(tds[year], year)
        tds[year]["teledeclaration.cout_denrees"] = tds[year].apply(
            lambda row: row["teledeclaration.value_total_ht"] / row["canteen.yearly_meal_count"], axis=1
        )
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
        cuisines_centrales = tds[year][tds[year]["canteen.production_type"].isin(["central_serving", "central"])]
        
        indicateurs[year]["Nombre de cantines sur place (sites et satellites)"] = len(cuisines_sur_place)
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

        indicateurs[year]["Taux de TD détaillées"] = len(
            tds[year][tds[year]["teledeclaration.diagnostic_type"] == "COMPLETE"]
        ) / len(tds[year])
    return pd.DataFrame(indicateurs)


def calcul_famille(df, famille='meat_poultry'):
    indicateurs = {}
    if famille == 'meat_poultry':
        label = 'Viande/Volaille 🥩'
    else:
        label = 'Poissons/Produits de la mer 🐟'

    df_famille = df.copy()[~df[f"teledeclaration.value_{famille}_ht"].isna()]
    
    indicateurs[f"Nombre de TD ayant déclaré pour la famille {label}"] = len(
        df_famille
    )
    indicateurs[f"Nombre de TD ayant déclaré la valeur 0€ pour la famille {label}"] = len(
        df_famille[df_famille[f"teledeclaration.value_{famille}_ht"] == 0]
    )
    indicateurs[f"Montant des achats alimentaires totaux pour la famille {label}"] = df_famille["teledeclaration.value_total_ht"].sum()
    
    indicateurs[f"Taux d'achat alimentaires de la famille {label}"] = int(
        df_famille[f"teledeclaration.value_{famille}_ht"].sum()
    ) / int(df_famille["teledeclaration.value_total_ht"].sum())
    indicateurs[f"Montant d'achat alimentaires {label}"] = int(
        df_famille[f"teledeclaration.value_{famille}_ht"].sum()
    )
    indicateurs[f"Taux d'achat alimentaires Egalim au sein de la famille {label}"] = int(
        df_famille[f"teledeclaration.value_{famille}_egalim_ht"].sum()
    ) / int(df_famille[f"teledeclaration.value_{famille}_ht"].sum())
    indicateurs[f"Montant d'achat alimentaires Egalim {label}"] = int(
        df_famille["teledeclaration.value_meat_poultry_egalim_ht"].sum()
    )
    if famille == 'meat_poultry':
        indicateurs[f"Taux d'achat alimentaires origine France 🇫🇷 au sein de la famille {label}"] = int(
            df_famille[f"teledeclaration.value_{famille}_france_ht"].sum()
        ) / int(df_famille[f"teledeclaration.value_{famille}_ht"].sum())
        indicateurs[f"Montant d'achat alimentaires origine France 🇫🇷 {label}"] = int(
            df_famille[f"teledeclaration.value_{famille}_france_ht"].sum()
        )
    return indicateurs


def calcul_indicateur_famille(tds: {}, years=[], col_comparaison=True):
    indicateurs = {}
    for year in years if len(years) else tds.keys():
        indicateurs[year] = {}
        indicateurs[year]["Nombre de TD prises en compte"] = len(tds[year])
        indicateurs[year].update(calcul_famille(tds[year], 'meat_poultry'))
        indicateurs[year].update(calcul_famille(tds[year], 'fish'))

    return pd.DataFrame(indicateurs)

# tds = {}
# tds['Campagne 2023'] = pd.read_csv("stats/bilan/data/export_dataset_stats_campagne_clean_2023.csv", sep=";")
# print(calcul_indicateur_famille(tds, ['Campagne 2023']))

def calcul_indicateur_appro(tds: {}, years=[], col_comparaison=True):
    indicateurs = {}
    for year in years if len(years) else tds.keys():

        indicateurs[year] = {}
        cuisines_sur_place = tds[year][tds[year]["canteen.production_type"].isin(["site", "site_cooked_elsewhere"])]
        cuisines_centrales = tds[year][tds[year]["canteen.production_type"].isin(["central_serving", "central"])]

        indicateurs[year]["Montant d'achat alimentaires total"] = int(
            tds[year]["teledeclaration.value_total_ht"].sum()
        )
        indicateurs[year]["Montant des achats alimentaires cuisines centrales"] = cuisines_centrales["teledeclaration.value_total_ht"].sum()
        indicateurs[year]["Montant des achats alimentaires cantines satellites"] = cuisines_sur_place["teledeclaration.value_total_ht"].sum()
        indicateurs[year]["Montant des achats alimentaires cantines gestion concédée"] = tds[year][tds[year]["canteen.management_type"] != "direct"]['teledeclaration.value_total_ht'].sum()
        indicateurs[year]["Montant des achats alimentaires cantines gestion directe"] = tds[year][tds[year]["canteen.management_type"] == "direct"]['teledeclaration.value_total_ht'].sum()

        indicateurs[year]["Taux global des achats en bio"] = (
            tds[year]["teledeclaration.value_bio_ht"].sum() / tds[year]["teledeclaration.value_total_ht"].sum()
        )
        indicateurs[year]["Montant d'achat alimentaires bio"] = int(tds[year]["teledeclaration.value_bio_ht"].sum())

        indicateurs[year]["Nombre de TD ayant déclaré 0€ d'achats en Bio"] = len(
            tds[year][tds[year]["teledeclaration.value_bio_ht"] == 0]
        )

        indicateurs[year]["Taux global des achats SIQO"] = (
            tds[year]["teledeclaration.value_sustainable_ht"].sum()
        ) / tds[year]["teledeclaration.value_total_ht"].sum()
        indicateurs[year]["Montant d'achat alimentaires SIQO"] = tds[year][
            "teledeclaration.value_sustainable_ht"
        ].sum()

        indicateurs[year]["Taux global des autres achats Egalim"] = (
            tds[year]["teledeclaration.value_egalim_others_ht"].sum()
        ) / tds[year]["teledeclaration.value_total_ht"].sum()
        indicateurs[year]["Montant des autres achats Egalim"] = tds[year][
            "teledeclaration.value_egalim_others_ht"
        ].sum()

        indicateurs[year]["Taux global des achats perf/ext"] = (
            tds[year]["teledeclaration.value_externality_performance_ht"].sum()
        ) / tds[year]["teledeclaration.value_total_ht"].sum()
        indicateurs[year]["Montant des achats perf/ext"] = tds[year][
            "teledeclaration.value_externality_performance_ht"
        ].sum()

        indicateurs[year]["Taux global des achats EGALIM (bio inclus)"] = (
            tds[year]["teledeclaration.value_egalim_others_ht"].sum()
            + tds[year]["teledeclaration.value_externality_performance_ht"].sum()
            + tds[year]["teledeclaration.value_bio_ht"].sum()
            + tds[year]["teledeclaration.value_sustainable_ht"].sum()
        ) / tds[year]["teledeclaration.value_total_ht"].sum()
        indicateurs[year]["Montant d'achat alimentaires bio"] = int(tds[year]["teledeclaration.value_bio_ht"].sum())

        indicateurs[year]["Montant d'achat alimentaires EGALIM (bio inclus)"] = (
            tds[year]["teledeclaration.value_egalim_others_ht"].sum()
            + tds[year]["teledeclaration.value_externality_performance_ht"].sum()
            + tds[year]["teledeclaration.value_bio_ht"].sum()
            + tds[year]["teledeclaration.value_sustainable_ht"].sum()
        )

    return pd.DataFrame(indicateurs)


def ajout_col_comparaison(indicateurs):
    if len(indicateurs.columns) != 2:
        print("Erreur : Il faut exactement 2 colonnes pour activer la comparaison")
    else:
        indicateurs["Comparaison"] = indicateurs[indicateurs.columns[1]] - indicateurs[indicateurs.columns[0]]
    return indicateurs


# Define custom formatter functions²
def nombre_formatter(value):
    # Your custom formatting logic here
    return f"{value:,.0f}".replace(",", " ")


def taux_formatter(value):
    # Your custom formatting logic here
    return f"{100 * value:.1f} %"


def points_formatter(value):
    # Your custom formatting logic here
    return f"{value:.2f} pts"


def montant_formatter(value):
    # Your custom formatting logic here
    return f"{value:,.0f} €".replace(",", " ")


def cout_formatter(value):
    # Your custom formatting logic here
    return f"{value:,.2f} €".replace(",", " ")


def apply_formatters(df):
    df[df.columns[df.columns.str.startswith("Taux")]] = df[df.columns[df.columns.str.startswith("Taux")]].applymap(
        taux_formatter
    )
    df[df.columns[df.columns.str.startswith("Montant")]] = df[
        df.columns[df.columns.str.startswith("Montant")]
    ].applymap(montant_formatter)
    df[df.columns[df.columns.str.startswith("Coût")]] = df[df.columns[df.columns.str.startswith("Coût")]].applymap(
        cout_formatter
    )
    df[df.columns[df.columns.str.startswith("Nombre")]] = df[df.columns[df.columns.str.startswith("Nombre")]].applymap(
        nombre_formatter
    )
    return df


def display_indicateurs(df, transpose=True, format=True, col_order=None):
    if isinstance(df, pd.Series):
        df = df.to_frame()
    if format:
        if transpose:
            df = df.T
        try:
            # df = df
            df = apply_formatters(df)
        except Exception:
            pass
        if transpose:
            df = df.T
        if isinstance(df, pd.DataFrame):
            if "Comparaison" in df.columns:
                df["Comparaison"] = df["Comparaison"].apply(lambda x: x.replace("%", "pts"))
    if col_order:
        print(df[col_order].to_html())
    else:
        print(df.to_html())


def display_stacked_bars(df, title="Comparaison entre les campagnes 2022 et 2023", fmt=nombre_formatter, legend=True, iso=True):
    # Choosing order of bars displaying
    if iso:
        ax = df.plot.barh(color=("#2f7569", "#063442"), figsize=(8, 6.0))
    else:
        ax = df.plot.barh(color=("#FFCE30", "#E83845"), figsize=(8, 6.0))
    for bars in ax.containers:
        ax.bar_label(bars, fmt=fmt, label_type="center", color="white", size=12, weight='bold')

    ax.set_title('Distribution des valeurs d\'achats en € totales et bio', fontsize='large')
    # ax.set_ylabel('Nombre de TD', fontsize='large')
    # ax.set_xlabel('Valeurs d\'achats en € (en log)', fontsize='large')

    ax.set_title('Distribution des valeurs d\'achats en € totales et bio', fontsize='large')
    ax.set_ylabel('Secteur', fontsize='large')
    ax.set_xlabel('Part des télédéclarants', fontsize='large')
    ax.set_title(title, size=12, weight='bold')
    if not legend:
        legend = ax.legend()
        legend.remove()



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
        columns={"2023": "Part des valeurs renseignées (2023)", "2022": "Part des valeurs renseignées (2022)"}
    )
    print(pourcentage_in_file_to_display.to_html())


def aggregate_geo(td, decoupage, value):
    tds_geo = {}
    cmap = ""
    if value == "nombre_td":
        cmap = "Blues"
        tds_geo = td.groupby(f"canteen.{decoupage}").count()
        tds_geo["value"] = tds_geo["canteen.id"]
    elif value == "taux_bio":
        cmap = "Greens"
        tds_geo = td.groupby(f"canteen.{decoupage}").sum()
        tds_geo["value"] = 100 * tds_geo["teledeclaration.value_bio_ht"] / tds_geo["teledeclaration.value_total_ht"]
    elif value == "Comparaison":
        cmap = "PRGn"
        tds_geo = td
        tds_geo = tds_geo.rename(columns={"Comparaison": "value"})
    else:
        print("Error : Wrong attribute")
    tds_geo = tds_geo.reset_index()
    tds_geo = tds_geo[["value", f"canteen.{decoupage}"]]
    return tds_geo, cmap


def display_map_(td, decoupage="department", value="nombre_td"):
    tds_geo, cmap = aggregate_geo(td, decoupage, value)
    tds_geo = tds_geo.dropna(subset=f"canteen.{decoupage}")
    if decoupage == "region":
        tds_geo[f"canteen.{decoupage}"] = tds_geo[f"canteen.{decoupage}"].apply(lambda x: f"{int(x):02d}")
    try:
        sf = gpd.read_file(f"france-geojson/{decoupage}s-version-simplifiee.geojson")
    except Exception:
        print(
            "Les contours des départements/régions doivent être téléchargés et déposes dans un dossier france-geojson \n"
        )
        print(
            "Lien Départements : https://github.com/gregoiredavid/france-geojson/blob/master/departements-version-simplifiee.geojson"
        )
        print(
            "Lien Départements : https://github.com/gregoiredavid/france-geojson/blob/master/regions-version-simplifiee.geojson"
        )
        return 0
    sf = pd.merge(sf, tds_geo[[f"canteen.{decoupage}", "value"]], left_on="code", right_on=f"canteen.{decoupage}")
    geo_element = gv.Polygons(sf, vdims=["nom", "value"])
    geo_element.opts(
        width=600,
        height=600,
        toolbar="above",
        color=dim("value"),
        colorbar=True,
        tools=["hover"],
        aspect="equal",
        cmap=cmap,
    )
    gv.output(geo_element)
    return sf


def fill_region(code_insee):
    try:
        url = f"https://geo.api.gouv.fr/regions/{code_insee}"
        res = requests.get(
            url,
        )
        return res.json()["nom"]
    except Exception as e:
        return "Erreur geo"


def fill_departement(code_insee):
    try:
        url = f"https://geo.api.gouv.fr/departements/{code_insee}"
        res = requests.get(
            url,
        )
        return res.json()["nom"]
    except Exception as e:
        return "Erreur geo"


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
        