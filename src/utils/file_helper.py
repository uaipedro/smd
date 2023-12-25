import os


def file_path_from_specie(specie: str) -> str:
    return f"{specie.lower().replace(' ', '_')}.xlsx"


def get_output_path(filename: str, format="") -> str:
    foldername = "../output"
    # Verifica se a pasta existe
    if not os.path.exists(foldername):
        # Se não existe, cria a pasta
        os.makedirs(foldername)
        print(f"A pasta {foldername} foi criada.")

    if format:
        filename = f"{filename}.{format}"

    return os.path.join(foldername, filename)
