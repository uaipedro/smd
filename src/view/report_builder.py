import pandas as pd

pd.set_option("display.float_format", "{:.2f}".format)


class ReportBuilder:
    def build(self, df: pd.DataFrame):
        return df.describe().transpose()

    def print(self, df: pd.DataFrame):
        print(self.build(df))
