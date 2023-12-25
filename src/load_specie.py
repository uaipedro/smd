import typer
from typing_extensions import Annotated

from src.bioclim.bioclim_service import BioclimService
from src.gbif.gbif_service import busca_especie_no_gbif
from src.utils.file_helper import file_path_from_specie
from src.utils.with_progress import with_progress
from src.view.file_writer import FileWriter
from src.view.map_builder import MapBuilder

app = typer.Typer()

busca = with_progress(busca_especie_no_gbif, "Buscando ocorrências no GBIF")
enriquece = with_progress(
    BioclimService().augment_data_with_bioclimate, "Enriquecendo dados com bioclima"
)
salva_dados = with_progress(FileWriter().write, "Salvando dados")
cria_mapa = with_progress(MapBuilder().build, "Criando mapa")


StrArg = Annotated[str, typer.Argument()]
StrOpt = Annotated[str, typer.Option()]
BoolOpt = Annotated[bool, typer.Option()]

"""
    Load species data from GBIF and enrich it with bioclimatic data.

    Args:
        specie (str): The name of the species to load.
        output_format (str, optional): The format to save the data in. Defaults to "xlsx".
        save_map (bool, optional): Whether to save a map of the species occurrences. Defaults to False.
"""


@app.command()
def load_specie(
    specie: StrArg,
    output_format: StrOpt = "xlsx",
    save_map: BoolOpt = False,
):
    path = file_path_from_specie(specie)
    ocorrencias = enriquece(busca(specie))
    salva_dados(ocorrencias, output_format, path)

    if save_map:
        cria_mapa(ocorrencias, path)


if __name__ == "__main__":
    app()
