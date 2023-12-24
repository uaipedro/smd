import time

import typer
from rich.progress import Progress, SpinnerColumn, TextColumn
from typing_extensions import Annotated

from smd.bioclim.bioclim_service import BioclimService
from smd.gbif.gbif_service import busca_especie_no_gbif
from smd.view.file_writer import FileWriter
from smd.view.map_builder import MapBuilder

app = typer.Typer()

# coords é um anotated typer Options que é uma lista de listas de floats
# https://typer.tiangolo.com/tutorial/options/annotated/


@app.command()
def load_specie(
    specie: Annotated[str, typer.Argument()],
    output: Annotated[str, typer.Option()] = "output",
    output_format: Annotated[str, typer.Option()] = "xlsx",
    save_map: Annotated[bool, typer.Option()] = False,
):
    typer.echo(f"Loading specie from gbif: {specie}")
    now = time.time()

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task_id = progress.add_task("Loading specie from gbif", total=None)
        occurrences = busca_especie_no_gbif(specie)
        progress.remove_task(task_id)

        task_id = progress.add_task("Augmenting data with bioclim", total=None)
        occurrences = BioclimService().augment_data_with_bioclimate(occurrences)
        progress.remove_task(task_id)

        if output == "output":
            output = specie.replace(" ", "_")

        fw = FileWriter()

        typer.echo(f"Finished loading specie {specie} in {time.time() - now} seconds")

        fw.write(occurrences, output_format, output)

        if save_map:
            mapa = MapBuilder().build(occurrences)
            mapa.save(f"data/{output}_ocurrences_map.html")

        # typer.echo(occurrences)


if __name__ == "__main__":
    app()
