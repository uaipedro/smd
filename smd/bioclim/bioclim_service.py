import fiona.transform
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
    def reproject_coords(self, src_crs, dst_crs, coords):
        xs = [c[0] for c in coords]
        ys = [c[1] for c in coords]
        xs, ys = fiona.transform.transform(src_crs, dst_crs, xs, ys)
        return [[x, y] for x, y in zip(xs, ys)]

    def layer_path(self, layer):
        return f"../data/bioclim/bioclim_{layer}.tif"

    def load_bioclimate_values(self, coords=[]):
        results = [{"lon": coord[0], "lat": coord[1]} for coord in coords]

        for index, (alias, name) in enumerate(BIOCLIM_LAYERS):
            with rasterio.open(self.layer_path(index)) as dataset:
                src_crs = "EPSG:4326"
                dst_crs = dataset.crs.to_epsg()
                # dst_crs = dataset.crs.to_wkt()  # 'PROJCS["World_Mollweide",GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS    84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0],UNIT["Degree",0.0174532925199433]],PROJECTION["Mollweide"],PARAMETER["central_meridian",0],PARAMETER["false_easting",0],PARAMETER["false_northing",0],UNIT["metre",1,AUTHORITY["EPSG","9001"]],AXIS["Easting",EAST],AXIS["Northing",NORTH]]'

                # [longitude, latitude] not [lat, lon]...
                new_coords = self.reproject_coords(src_crs, dst_crs, coords)

                values = list(rasterio.sample.sample_gen(dataset, new_coords))

                for idx, ((lon, lat), value) in enumerate(zip(coords, values)):
                    print(lon, lat, value[0])  # value[0] == band 1 value at lon, lat
                    results[idx - 1][f"{alias}"] = value[0]

        self.bioclim_data = results

    def get_bioclimate_values(self):
        if not hasattr(self, "bioclim_data"):
            self.load_bioclimate_values()
        return self.bioclim_data
