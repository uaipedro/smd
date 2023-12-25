import fiona.transform
import pandas as pd
import rasterio.sample

BIOCLIM_LAYERS = [
    ("BIO1", "Annual Mean Temperature"),
    ("BIO2", "Mean Diurnal Range (Mean of monthly (max temp - min temp))"),
    ("BIO3", "Isothermality (BIO2/BIO7) (×100)"),
    ("BIO4", "Temperature Seasonality (standard deviation ×100)"),
    ("BIO5", "Max Temperature of Warmest Month"),
    ("BIO6", "Min Temperature of Coldest Month"),
    ("BIO7", "Temperature Annual Range (BIO5-BIO6)"),
    ("BIO8", "Mean Temperature of Wettest Quarter"),
    ("BIO9", "Mean Temperature of Driest Quarter"),
    ("BIO10", "Mean Temperature of Warmest Quarter"),
    ("BIO11", "Mean Temperature of Coldest Quarter"),
    ("BIO12", "Annual Precipitation"),
    ("BIO13", "Precipitation of Wettest Month"),
    ("BIO14", "Precipitation of Driest Month"),
    ("BIO15", "Precipitation Seasonality (Coefficient of Variation)"),
    ("BIO16", "Precipitation of Wettest Quarter"),
    ("BIO17", "Precipitation of Driest Quarter"),
    ("BIO18", "Precipitation of Warmest Quarter"),
    ("BIO19", "Precipitation of Coldest Quarter"),
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

    def augment_data_with_bioclimate(self, dataframe: pd.DataFrame):
        dataframe.rename(
            columns={"decimalLongitude": "lon", "decimalLatitude": "lat"}, inplace=True
        )

        coords = list(zip(dataframe.lon, dataframe.lat))

        for index, (alias, _) in enumerate(BIOCLIM_LAYERS):
            with rasterio.open(self.layer_path(index)) as raster:
                reprojected_coords = self.reproject_coords(raster, coords)

                values = list(rasterio.sample.sample_gen(raster, reprojected_coords))

                for idx, ((lon, lat), value) in enumerate(zip(coords, values)):
                    dataframe.loc[idx, alias] = value[0]

        return dataframe
