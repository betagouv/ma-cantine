from django.db import models


def get_lib_region_from_code(region: str) -> str:
    if region and (region in Region):
        return Region(region).label.split(" - ")[1]


class Region(models.TextChoices):
    guadeloupe = "01", "01 - Guadeloupe"
    martinique = "02", "02 - Martinique"
    guyane = "03", "03 - Guyane"
    la_reunion = "04", "04 - La Réunion"
    mayotte = "06", "06 - Mayotte"
    ile_de_france = "11", "11 - Île-de-France"
    centre_val_de_loire = "24", "24 - Centre-Val de Loire"
    bourgogne_franche_comte = "27", "27 - Bourgogne-Franche-Comté"
    normandie = "28", "28 - Normandie"
    hauts_de_france = "32", "32 - Hauts-de-France"
    grand_est = "44", "44 - Grand Est"
    pays_de_la_loire = "52", "52 - Pays de la Loire"
    bretagne = "53", "53 - Bretagne"
    nouvelle_aquitaine = "75", "75 - Nouvelle-Aquitaine"
    occitanie = "76", "76 - Occitanie"
    auvergne_rhone_alpes = "84", "84 - Auvergne-Rhône-Alpes"
    provence_alpes_cote_d_azur = "93", "93 - Provence-Alpes-Côte d'Azur"
    corse = "94", "94 - Corse"
    saint_pierre_et_miquelon = "975", "975 - Saint-Pierre-et-Miquelon"
    saint_barthelemy = "977", "977 - Saint-Barthélemy"
    saint_martin = "978", "978 - Saint-Martin"
    terres_australes_et_antarctiques_francaises = "984", "984 - Terres australes et antarctiques françaises"
    wallis_et_futuna = "986", "986 - Wallis-et-Futuna"
    polynesie_francaise = "987", "987 - Polynésie Française"
    nouvelle_caledonie = "988", "988 - Nouvelle Calédonie"
    ile_de_clipperton = "989", "989 - Île de Clipperton"


REGION_HEXAGONE_LIST = [
    Region.ile_de_france,
    Region.centre_val_de_loire,
    Region.bourgogne_franche_comte,
    Region.normandie,
    Region.hauts_de_france,
    Region.grand_est,
    Region.pays_de_la_loire,
    Region.bretagne,
    Region.nouvelle_aquitaine,
    Region.occitanie,
    Region.auvergne_rhone_alpes,
    Region.provence_alpes_cote_d_azur,
    Region.corse,
]
