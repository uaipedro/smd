import typer
from typing_extensions import Annotated

from src.bioclim.bioclim_service import BIOCLIM_LAYERS, BioclimService
from src.gbif.gbif_service import busca_especie_no_gbif
from src.utils.file_helper import file_path_from_specie
from src.utils.stats_helper import remove_outliers
from src.utils.with_progress import with_progress
from src.view.file_writer import FileWriter
from src.view.map_builder import MapBuilder
from src.view.report_builder import ReportBuilder

app = typer.Typer()

busca = with_progress(busca_especie_no_gbif, "Buscando ocorrências no GBIF")
enriquece = with_progress(
    BioclimService().augment_data_with_bioclimate, "Enriquecendo dados com bioclima"
)
salva_dados = with_progress(FileWriter().write, "Salvando dados")
cria_mapa = with_progress(MapBuilder().build, "Criando mapa")
cria_relatorio = with_progress(ReportBuilder().build, "Criando relatório")
imprime_relatorio = with_progress(ReportBuilder().print, "Imprimindo relatório")
traduz_camadas = with_progress(
    BioclimService().translate_layers_inplace, "Traduzindo camadas"
)

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
    verbose: BoolOpt = False,
    drop_empty: BoolOpt = False,
    drop_outliners: BoolOpt = False,
    layer_pt_br: BoolOpt = False,
):
    path = file_path_from_specie(specie)

    ocorrencias = busca(specie)

    ocorrencias_ricas = enriquece(ocorrencias)

    if drop_empty:
        ocorrencias_ricas.dropna(inplace=True)

    if drop_outliners:
        ocorrencias_ricas = remove_outliers(
            ocorrencias_ricas, [f"BIO{i+1}" for i in range(19)]
        )

    if layer_pt_br:
        traduz_camadas(ocorrencias_ricas)

    if save_map:
        cria_mapa(ocorrencias_ricas, path)

    if verbose:
        imprime_relatorio(ocorrencias_ricas)

    salva_dados(ocorrencias_ricas, output_format, path)


if __name__ == "__main__":
    app()
