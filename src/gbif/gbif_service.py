import pandas as pd
from pygbif import occurrences as occ


def busca_especie_no_gbif(nome_cientifico, country=None, size=100):
    infos_interesse = [
        "taxonKey",
        "genus",
        "species",
        "decimalLatitude",
        "decimalLongitude",
        "country",
        # "coordinateUncertaintyInMeters",
        "year",
        # "month",
        # "day",
    ]

    complete = []
    page = 0
    while True:
        results = occ.search(
            scientificName=nome_cientifico,
            limit=300,
            offset=300 * page,
            hasCoordinate=True,
            country=country,
        ).get("results")
        complete = [*complete, *results]
        if len(results) < 300:
            break
        page += 1

    df = pd.DataFrame(complete)

    return df[infos_interesse]
