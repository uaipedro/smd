import fiona.transform
import pandas as pd
import rasterio.sample

BIOCLIM_LAYERS = [
    {
        "short": "BIO1",
        "full": "Annual Mean Temperature",
        "pt-br": "Temperatura Média Anual",
    },
    {
        "short": "BIO2",
        "full": "Mean Diurnal Range (Mean of monthly (max temp - min temp))",
        "pt-br": "Variação Diurna Média (Média mensal (temp máx - temp mín))",
    },
    {
        "short": "BIO3",
        "full": "Isothermality (BIO2/BIO7) (×100)",
        "pt-br": "Isotermalidade (BIO2/BIO7) (×100)",
    },
    {
        "short": "BIO4",
        "full": "Temperature Seasonality (standard deviation ×100)",
        "pt-br": "Seasonalidade da Temperatura (desvio padrão ×100)",
    },
    {
        "short": "BIO5",
        "full": "Max Temperature of Warmest Month",
        "pt-br": "Temperatura Máxima do Mês Mais Quente",
    },
    {
        "short": "BIO6",
        "full": "Min Temperature of Coldest Month",
        "pt-br": "Temperatura Mínima do Mês Mais Frio",
    },
    {
        "short": "BIO7",
        "full": "Temperature Annual Range (BIO5-BIO6)",
        "pt-br": "Variação Anual da Temperatura (BIO5-BIO6)",
    },
    {
        "short": "BIO8",
        "full": "Mean Temperature of Wettest Quarter",
        "pt-br": "Temperatura Média do Trimestre Mais Chuvoso",
    },
    {
        "short": "BIO9",
        "full": "Mean Temperature of Driest Quarter",
        "pt-br": "Temperatura Média do Trimestre Mais Seco",
    },
    {
        "short": "BIO10",
        "full": "Mean Temperature of Warmest Quarter",
        "pt-br": "Temperatura Média do Trimestre Mais Quente",
    },
    {
        "short": "BIO11",
        "full": "Mean Temperature of Coldest Quarter",
        "pt-br": "Temperatura Média do Trimestre Mais Frio",
    },
    {"short": "BIO12", "full": "Annual Precipitation", "pt-br": "Precipitação Anual"},
    {
        "short": "BIO13",
        "full": "Precipitation of Wettest Month",
        "pt-br": "Precipitação do Mês Mais Chuvoso",
    },
    {
        "short": "BIO14",
        "full": "Precipitation of Driest Month",
        "pt-br": "Precipitação do Mês Mais Seco",
    },
    {
        "short": "BIO15",
        "full": "Precipitation Seasonality (Coefficient of Variation)",
        "pt-br": "Seasonalidade da Precipitação (Coeficiente de Variação)",
    },
    {
        "short": "BIO16",
        "full": "Precipitation of Wettest Quarter",
        "pt-br": "Precipitação do Trimestre Mais Chuvoso",
    },
    {
        "short": "BIO17",
        "full": "Precipitation of Driest Quarter",
        "pt-br": "Precipitação do Trimestre Mais Seco",
    },
    {
        "short": "BIO18",
        "full": "Precipitation of Warmest Quarter",
        "pt-br": "Precipitação do Trimestre Mais Quente",
    },
    {
        "short": "BIO19",
        "full": "Precipitation of Coldest Quarter",
        "pt-br": "Precipitação do Trimestre Mais Frio",
    },
]


class BioclimService:
    def reproject_coords(self, dataset, coords):
        src_crs = "EPSG:4326"
        dst_crs = dataset.crs.to_epsg()
        xs = [c[0] for c in coords]
        ys = [c[1] for c in coords]
        xs, ys = fiona.transform.transform(src_crs, dst_crs, xs, ys)
        return [[x, y] for x, y in zip(xs, ys)]

    def layer_path(self, layer):
        return f"bioclim/data/wc2.1_5m_bio_{layer+1}.tif"

    def augment_data_with_bioclimate(
        self, dataframe: pd.DataFrame, layer_alias="short"
    ):
        dataframe.rename(
            columns={"decimalLongitude": "lon", "decimalLatitude": "lat"}, inplace=True
        )

        coords = list(zip(dataframe.lon, dataframe.lat))

        for index, layer_name in enumerate(BIOCLIM_LAYERS):
            with rasterio.open(self.layer_path(index)) as raster:
                reprojected_coords = self.reproject_coords(raster, coords)

                values = list(rasterio.sample.sample_gen(raster, reprojected_coords))

                for idx, ((lon, lat), value) in enumerate(zip(coords, values)):
                    dataframe.loc[idx, layer_name[layer_alias]] = value[0]

        return dataframe

    def translate_layers_inplace(
        self, df: pd.DataFrame, old_alias="short", new_alias="pt-br"
    ):
        for layer in BIOCLIM_LAYERS:
            df.rename(columns={layer[old_alias]: layer[new_alias]}, inplace=True)
