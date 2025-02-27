def normalise_siret(siret):
    return siret.replace(" ", "").replace("\xa0", "")


def is_valid_siret(siret: str) -> bool:
    if len(siret) == 14:
        return True
