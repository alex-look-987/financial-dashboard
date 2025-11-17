import numpy as np
import pandas as pd
from typing import Tuple
from ta.momentum import rsi
from ta.volatility import AverageTrueRange
from production.technical_indicators import ma_computation

TARGET = 'mean'
FEATURE, WINDOW = ['close'], [3, 5, 8]

ATR_WINDOW = 5
RSI_TARGER = 'high'
RSI_WINDOW, RSI_MA_WINDOW = 5, 5

sub_indicators = ['rsi', 'atr']

def data_processor(df: pd.DataFrame, over_ti: str, sub_ti: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Función para generar etiquetas de colores para el gráfico de velas
    y dataframe para graficar el ZigZag
    
    Args:
        df (_dataframe_): _date, OHLC, zz_
        
    Returns:
        _pd.Dataframe_: df_candle = date, OHLC, zz, color
        _pd.Dataframe_: df_zz = date, zz_line
    """       
    
    df['date'] = pd.to_datetime(df['date'])
    df['color'] = np.where(df['open'] < df['close'], 'orange', 'white')

    over_cols = [col for col in df.columns if over_ti in col]
    sub_cols = [col for col in df.columns if any(k in col for k in sub_ti)]

    sub_cols.append('date')

    overlay_ti = df[over_cols].copy()
    subpanel_ti = df[sub_cols].copy()

    return df, overlay_ti, subpanel_ti

def process_data(file: str):
    df = pd.read_csv(file)
    
    float_cols = df.select_dtypes(include=['float64']).columns
    df[float_cols] = df[float_cols].astype('float32')
        
    df = ma_computation(df, TARGET , FEATURE, WINDOW)

    df["rsi"] = rsi(df[RSI_TARGER], RSI_WINDOW)
    df['rsi_ma'] = df['rsi'].rolling(RSI_MA_WINDOW).mean()

    atr = AverageTrueRange(
        high=df["high"],
        low=df["low"],
        close=df["close"],
        window=ATR_WINDOW)

    df["atr"] = atr.average_true_range()

    df, overlay_ti, sub_ti = data_processor(df, TARGET , sub_indicators)

    return df, overlay_ti, sub_ti
