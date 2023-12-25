import folium
import pandas as pd

from src.utils.file_helper import get_output_path


class MapBuilder:
    def build(self, dataframe: pd.DataFrame, output: str = None) -> folium.Map:
        mapa = folium.Map(
            location=[
                dataframe["lat"].mean(),
                dataframe["lon"].mean(),
            ],
            zoom_start=5,
        )

        # Adicionar marcadores para cada ponto no DataFrame
        for index, row in dataframe.iterrows():
            folium.Marker(location=[row["lat"], row["lon"]]).add_to(mapa)

        if output:
            mapa.save(get_output_path(output, "html"))

        return mapa
