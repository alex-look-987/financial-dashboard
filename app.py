import sys
import pandas as pd
from bokeh.io import curdoc
from dashboard.themes import *
from bokeh.themes import Theme
from typing import Dict, Tuple
from bokeh.layouts import column
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from dashboard.processing import process_data
from dashboard.plots import candlestick_plot, subpanel_plot

STYLE = dark_theme
 
contract = str(sys.argv[1]).lower()
timeframes = ["1min", "15mins", "1hour", "4hours", "1day", "1week", "1month"]

xaxes: Dict[str, figure] = {}
plots: Dict[str, Tuple[figure, ...]] = {}
sources: Dict[str, Dict[str, ColumnDataSource]] = {}
dfs: Dict[str, Tuple[pd.DataFrame, pd.DataFrame]] = {}

for tf in timeframes:
    df_candle, overlay, subpanel = process_data(f"{contract}_{tf}.csv")

    candlestick, candle, src_over = candlestick_plot(df_candle, overlay)
    candlestick, p_rgb, src_rgb, p_avgr, src_avgr = subpanel_plot(candlestick, subpanel, ('rsi', 'atr'))
    
    plots[tf] = (candlestick, p_rgb, p_avgr)

    sources[tf] = {
        "candle": candle, "overlay": src_over,
        "rgb": src_rgb, "avgr": src_avgr,
        }
    
    xaxes[tf] = p_avgr
    dfs[tf] = (df_candle, overlay)

def update():
    try:
        for tf in timeframes:
            df_candle, overlay, subpanel = process_data(f"{contract}_{tf}.csv")
            
            dfs[tf] = (df_candle, overlay)

            sources[tf]["candle"].data = df_candle
            sources[tf]["overlay"].data = overlay
            sources[tf]["rgb"].data = subpanel
            sources[tf]["avgr"].data = subpanel

            p_avgr = xaxes[tf]
            p_avgr.xaxis.major_label_overrides = {i: date.strftime('%d/%m/%Y %H:%M:%S') for i, date in enumerate(df_candle["date"])}

    except pd.errors.EmptyDataError:
        pass

charts = [item for tf in timeframes for item in plots[tf]]

layout = column(*charts, sizing_mode="stretch_both")

curdoc().add_root(layout)

curdoc().theme = Theme(json=STYLE)
curdoc().title = contract.upper()

curdoc().add_periodic_callback(update, 10)