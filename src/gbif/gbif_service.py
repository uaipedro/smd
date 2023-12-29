import concurrent.futures

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
        "year",
    ]

    def count_pages():
        return occ.search(
            scientificName=nome_cientifico,
            limit=1,
            hasCoordinate=True,
            country=country,
        ).get("count")

    complete = []
    pages = count_pages() // size
    page_size = 300

    print("páginas:", pages)

    def search_page(offset):
        results = occ.search(
            scientificName=nome_cientifico,
            limit=page_size,
            offset=offset,
            hasCoordinate=True,
            country=country,
        ).get("results")
        return results

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Mapeie a função de busca para todas as páginas em paralelo
        all_results = executor.map(
            search_page, range(0, page_size * pages - 1, page_size)
        )

    # Combine os resultados de todas as páginas
    complete = [result for results in all_results for result in results]

    df = pd.DataFrame(complete)

    return df[infos_interesse]
