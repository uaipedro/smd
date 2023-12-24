from pprint import pprint

import typer
from typing_extensions import Annotated

from smd.gbif.gbif_service import busca_especie_no_gbif

app = typer.Typer()

# coords é um anotated typer Options que é uma lista de listas de floats
# https://typer.tiangolo.com/tutorial/options/annotated/


@app.command()
def load_specie(
    specie: Annotated[str, typer.Argument()],
    output: Annotated[str, typer.Option(prompt=True)],
):
    typer.echo(f"Loading specie from gbif: {specie}")
    occurrences = busca_especie_no_gbif(specie)

    occurrences.to_csv(output, index=False)
    pprint(occurrences)


if __name__ == "__main__":
    app()
