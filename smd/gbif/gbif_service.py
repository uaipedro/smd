import pandas as pd
from pygbif import occurrences as occ


def busca_especie_no_gbif(nome_cientifico, size=100):
    infos_interesse = [
        "taxonKey",
        "genus",
        "species",
        "decimalLatitude",
        "decimalLongitude",
        "country",
        "coordinateUncertaintyInMeters",
        "year",
        "month",
        "day",
    ]

    complete = []
    for page in range(int(size / 300) + 1):
        results = occ.search(
            scientificName=nome_cientifico,
            limit=300,
            offset=300 * page,
            hasCoordinate=True,
            country="BR",
        ).get("results")
        complete = [*complete, *results]

    df = pd.DataFrame(complete)

    return df[infos_interesse]
