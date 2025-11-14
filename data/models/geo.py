"""
Fichier pour stocker les Departements & Regions.
Il y a aussi de la logique géographique dans /common/api/decoupage_administratif.py
"""

from django.db import models


class Department(models.TextChoices):
    ain = "01", "01 - Ain"
    aisne = "02", "02 - Aisne"
    allier = "03", "03 - Allier"
    alpes_de_haute_provence = "04", "04 - Alpes-de-Haute-Provence"
    hautes_alpes = "05", "05 - Hautes-Alpes"
    alpes_maritimes = "06", "06 - Alpes-Maritimes"
    ardeche = "07", "07 - Ardèche"
    ardennes = "08", "08 - Ardennes"
    ariege = "09", "09 - Ariège"
    aube = "10", "10 - Aube"
    aude = "11", "11 - Aude"
    aveyron = "12", "12 - Aveyron"
    bouches_du_rhone = "13", "13 - Bouches-du-Rhône"
    calvados = "14", "14 - Calvados"
    cantal = "15", "15 - Cantal"
    charente = "16", "16 - Charente"
    charente_maritime = "17", "17 - Charente-Maritime"
    cher = "18", "18 - Cher"
    correze = "19", "19 - Corrèze"
    cote_d_or = "21", "21 - Côte-d'or"
    cotes_d_armor = "22", "22 - Côtes-d'armor"
    creuse = "23", "23 - Creuse"
    dordogne = "24", "24 - Dordogne"
    doubs = "25", "25 - Doubs"
    drome = "26", "26 - Drôme"
    eure = "27", "27 - Eure"
    eure_et_loir = "28", "28 - Eure-et-Loir"
    finistere = "29", "29 - Finistère"
    corse_du_sud = "2A", "2A - Corse-du-Sud"
    haute_corse = "2B", "2B - Haute-Corse"
    gard = "30", "30 - Gard"
    haute_garonne = "31", "31 - Haute-Garonne"
    gers = "32", "32 - Gers"
    gironde = "33", "33 - Gironde"
    herault = "34", "34 - Hérault"
    ille_et_vilaine = "35", "35 - Ille-et-Vilaine"
    indre = "36", "36 - Indre"
    indre_et_loire = "37", "37 - Indre-et-Loire"
    isere = "38", "38 - Isère"
    jura = "39", "39 - Jura"
    landes = "40", "40 - Landes"
    loir_et_cher = "41", "41 - Loir-et-Cher"
    loire = "42", "42 - Loire"
    haute_loire = "43", "43 - Haute-Loire"
    loire_atlantique = "44", "44 - Loire-Atlantique"
    loiret = "45", "45 - Loiret"
    lot = "46", "46 - Lot"
    lot_et_garonne = "47", "47 - Lot-et-Garonne"
    lozere = "48", "48 - Lozère"
    maine_et_loire = "49", "49 - Maine-et-Loire"
    manche = "50", "50 - Manche"
    marne = "51", "51 - Marne"
    haute_marne = "52", "52 - Haute-Marne"
    mayenne = "53", "53 - Mayenne"
    meurthe_et_moselle = "54", "54 - Meurthe-et-Moselle"
    meuse = "55", "55 - Meuse"
    morbihan = "56", "56 - Morbihan"
    moselle = "57", "57 - Moselle"
    nievre = "58", "58 - Nièvre"
    nord = "59", "59 - Nord"
    oise = "60", "60 - Oise"
    orne = "61", "61 - Orne"
    pas_de_calais = "62", "62 - Pas-de-Calais"
    puy_de_dome = "63", "63 - Puy-de-Dôme"
    pyrenees_atlantiques = "64", "64 - Pyrénées-Atlantiques"
    hautes_pyrenees = "65", "65 - Hautes-Pyrénées"
    pyrenees_orientales = "66", "66 - Pyrénées-Orientales"
    bas_rhin = "67", "67 - Bas-Rhin"
    haut_rhin = "68", "68 - Haut-Rhin"
    rhone = "69", "69 - Rhône"
    haute_saone = "70", "70 - Haute-Saône"
    saone_et_loire = "71", "71 - Saône-et-Loire"
    sarthe = "72", "72 - Sarthe"
    savoie = "73", "73 - Savoie"
    haute_savoie = "74", "74 - Haute-Savoie"
    paris = "75", "75 - Paris"
    seine_maritime = "76", "76 - Seine-Maritime"
    seine_et_marne = "77", "77 - Seine-et-Marne"
    yvelines = "78", "78 - Yvelines"
    deux_sevres = "79", "79 - Deux-Sèvres"
    somme = "80", "80 - Somme"
    tarn = "81", "81 - Tarn"
    tarn_et_garonne = "82", "82 - Tarn-et-Garonne"
    var = "83", "83 - Var"
    vaucluse = "84", "84 - Vaucluse"
    vendee = "85", "85 - Vendée"
    vienne = "86", "86 - Vienne"
    haute_vienne = "87", "87 - Haute-Vienne"
    vosges = "88", "88 - Vosges"
    yonne = "89", "89 - Yonne"
    territoire_de_belfort = "90", "90 - Territoire de Belfort"
    essonne = "91", "91 - Essonne"
    hauts_de_seine = "92", "92 - Hauts-de-Seine"
    seine_saint_denis = "93", "93 - Seine-Saint-Denis"
    val_de_marne = "94", "94 - Val-de-Marne"
    val_d_oise = "95", "95 - Val-d'oise"
    guadeloupe = "971", "971 - Guadeloupe"
    martinique = "972", "972 - Martinique"
    guyane = "973", "973 - Guyane"
    la_reunion = "974", "974 - La Réunion"
    saint_pierre_et_miquelon = "975", "975 - Saint-Pierre-et-Miquelon"
    mayotte = "976", "976 - Mayotte"
    saint_barthelemy = "977", "977 - Saint-Barthélemy"
    saint_martin = "978", "978 - Saint-Martin"
    terres_australes_et_antarctiques_francaises = "984", "984 - Terres australes et antarctiques françaises"
    wallis_et_futuna = "986", "986 - Wallis-et-Futuna"
    polynesie_francaise = "987", "987 - Polynésie Française"
    nouvelle_caledonie = "988", "988 - Nouvelle Calédonie"
    ile_de_clipperton = "989", "989 - Île de Clipperton"


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


def get_lib_department_from_code(department: str) -> str:
    if department and (department in Department):
        return Department(department).label.split(" - ")[1]


def get_lib_region_from_code(region: str) -> str:
    if region and (region in Region):
        return Region(region).label.split(" - ")[1]


def get_region_from_department(department_code):
    code_department_to_region = {
        Department.ain: Region.auvergne_rhone_alpes,
        "02": "32",
        "03": "84",
        "04": "93",
        "05": "93",
        "06": "93",
        "07": "84",
        "08": "44",
        "09": "76",
        "10": "44",
        "11": "76",
        "12": "76",
        "13": "93",
        "14": "28",
        "15": "84",
        "16": "75",
        "17": "75",
        "18": "24",
        "19": "75",
        "21": "27",
        "22": "53",
        "23": "75",
        "24": "75",
        "25": "27",
        "26": "84",
        "27": "28",
        "28": "24",
        "29": "53",
        "2A": "94",
        "2B": "94",
        "30": "76",
        "31": "76",
        "32": "76",
        "33": "75",
        "34": "76",
        "35": "53",
        "36": "24",
        "37": "24",
        "38": "84",
        "39": "27",
        "40": "75",
        "41": "24",
        "42": "84",
        "43": "84",
        "44": "52",
        "45": "24",
        "46": "76",
        "47": "75",
        "48": "76",
        "49": "52",
        "50": "28",
        "51": "44",
        "52": "44",
        "53": "52",
        "54": "44",
        "55": "44",
        "56": "53",
        "57": "44",
        "58": "27",
        "59": "32",
        "60": "32",
        "61": "28",
        "62": "32",
        "63": "84",
        "64": "75",
        "65": "76",
        "66": "76",
        "67": "44",
        "68": "44",
        "69": "84",
        "70": "27",
        "71": "27",
        "72": "52",
        "73": "84",
        "74": "84",
        "75": "11",
        "76": "28",
        "77": "11",
        "78": "11",
        "79": "75",
        "80": "32",
        "81": "76",
        "82": "76",
        "83": "93",
        "84": "93",
        "85": "52",
        "86": "75",
        "87": "75",
        "88": "44",
        "89": "27",
        "90": "27",
        "91": "11",
        "92": "11",
        "93": "11",
        "94": "11",
        "95": "11",
        "971": "01",
        "972": "02",
        "973": "03",
        "974": "04",
        "976": "06",
        "975": "975",
        "977": "977",
        "978": "978",
        "984": "984",
        "986": "986",
        "987": "987",
        "988": "988",
        "989": "989",
    }
    if department_code and department_code in code_department_to_region:
        return code_department_to_region[department_code]
