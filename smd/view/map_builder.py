import folium
import pandas as pd


class MapBuilder:
    def build(self, dataframe: pd.DataFrame) -> folium.Map:
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

        return mapa
