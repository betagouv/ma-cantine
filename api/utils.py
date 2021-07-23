def normalise_siret(siret):
    return siret.replace(" ", "")


# TODO: API : https://entreprise.data.gouv.fr/api/sirene/v3/etablissements/{siret} : 7 appels/sec
# https://entreprise.data.gouv.fr/api_doc/sirene
