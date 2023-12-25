import numpy as np
import pandas as pd
from scipy import stats


def remove_outliers(df, columns, z_threshold=3):
    # Seleciona apenas as colunas desejadas
    subset_df = df[columns]

    # Calcule o Z-Score para cada ponto de dados nas colunas selecionadas
    z_scores = np.abs(stats.zscore(subset_df))

    # Defina um limite para considerar os pontos como outliers
    df_without_outliers = df[(z_scores < z_threshold).all(axis=1)]

    return df_without_outliers
