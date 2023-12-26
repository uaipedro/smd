import pandas as pd

pd.set_option("display.float_format", "{:.2f}".format)


class ReportBuilder:
    def build(self, df: pd.DataFrame):
        excluded_columns = [
            "taxonKey",
            "genus",
            "species",
            "country",
            "lat",
            "lon",
            "coordinateUncertaintyInMeters",
            "year",
            "month",
            "day",
        ]

        included_columns = [col for col in df.columns if col not in excluded_columns]

        return df.describe(include="all")[included_columns].transpose()

    def print(self, df: pd.DataFrame):
        print(self.build(df))
