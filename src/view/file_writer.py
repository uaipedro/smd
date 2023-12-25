import pandas as pd

from src.utils.file_helper import get_output_path


class FileWriter:
    def __init__(self) -> None:
        self.save_funcs = {
            "csv": self.save_csv,
            "json": self.save_json,
            "xlsx": self.save_xlsx,
        }

    def write(self, df: pd.DataFrame, format: str, output: str):
        self.save_funcs[format](df, output)

    def save_csv(self, df: pd.DataFrame, output: str):
        df.to_csv(get_output_path(output, "csv"), index=False)

    def save_json(self, df: pd.DataFrame, output: str):
        df.to_json(get_output_path(output, "json"), orient="records")

    def save_xlsx(self, df: pd.DataFrame, output: str):
        df.to_excel(get_output_path(output, "xlsx"), index=False)
