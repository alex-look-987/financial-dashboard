import numpy as np
import pandas as pd
from itertools import product

agg_funcs = {
    'mean': lambda s, w: pd.Series(s).rolling(w).mean(),
    'std': lambda s, w: pd.Series(s).rolling(w).std(),
    'sum': lambda s, w: pd.Series(s).rolling(w).sum(),
    'max': lambda s, w: pd.Series(s).rolling(w).max(),
    'min': lambda s, w: pd.Series(s).rolling(w).min(),
    'median': lambda s, w: pd.Series(s).rolling(w).median(),
    'skew': lambda s, w: pd.Series(s).rolling(w).skew(),
    'diff': lambda s, w: pd.Series(s).diff(w-1),
    'pct_change': lambda s, w: pd.Series(s).pct_change()}

def ma_computation(df: pd.DataFrame, func_name: str, feature: list, window: list):

    for window, feature in product(window, feature):
        col_name = f'{feature}_{func_name}_{window}'

        df[col_name] = agg_funcs[func_name](df[feature], window)

    df.dropna(inplace=True)
    df = df.round(5)

    return df
