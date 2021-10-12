from django.db import models


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
