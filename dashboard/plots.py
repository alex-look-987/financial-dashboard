import pandas as pd
from typing import Tuple
from bokeh.plotting import figure
from bokeh.palettes import Category10
from bokeh.models import ColumnDataSource, HoverTool, CrosshairTool, BasicTicker

WINDOWS = 96

def candlestick_plot(df: pd.DataFrame, overlay_ti: pd.DataFrame, subopanel_ti: pd.DataFrame, sub_order: tuple) -> \
Tuple[figure, ColumnDataSource, ColumnDataSource, figure, ColumnDataSource, figure, ColumnDataSource, ColumnDataSource, ColumnDataSource]:
    """Creación gráfico de velas y zigzag, y objetos respectivos para su actualización tiempo real .
    Candlestick: figura que contiene gráfica de velas y línea para zz
    source_candle: objeto para gráfico de velas utilizado para actualización en tiempo real
    source_over: objeto para gráfico de zigzag utilizado para actualización en tiempo real

    Args:
        df_candle (pd.DataFrame): _date, OHLC, color_
        df_zz (pd.DataFrame): _date, zz_line_

    Returns:
        Tuple[figure, ColumnDataSource, ColumnDataSource]: __candlestick, source_candle, source_over_
    """

    source_candle: ColumnDataSource = ColumnDataSource(df)
    source_over: ColumnDataSource = ColumnDataSource(overlay_ti)

    # === Initial Config === #
    dashboard: figure = figure(
        tools="pan, wheel_zoom, xwheel_zoom, ywheel_zoom, reset, xwheel_pan",
        width=1750, height=550, toolbar_location='right', active_drag='pan', active_scroll='wheel_zoom',
        x_axis_type='datetime', y_axis_location='right', output_backend="webgl")

    # === Ranges === #
    dashboard.x_range.follow = "end"
    dashboard.xaxis.visible = False
    dashboard.x_range.follow_interval = WINDOWS
    dashboard.x_range.range_padding = 0.003

    # === Grid/Ticks === #
    dashboard.grid.grid_line_color = 'black'
    ticker = BasicTicker(desired_num_ticks=10)
    dashboard.xgrid.ticker = ticker
    dashboard.ygrid.ticker = ticker

    crosshair = CrosshairTool(line_color="white")  # puedes usar hex o nombres de color
    dashboard.add_tools(crosshair)

    # Candlestick
    dashboard.segment(x0='index', y0='high', x1='index', y1='low', color='color', source=source_candle)
    render = dashboard.vbar(x='index', width=0.95, top='open', bottom='close', fill_color='color', line_color="color", source=source_candle)    

    # Overlay Indicators
    palette = Category10[len(overlay_ti.columns)]

    for col, color in zip(overlay_ti, palette):
        dashboard.line(
            x='index',
            y=col,
            source=source_over,
            line_width=2.3,
            line_color=color)

    # === Hover Tool === #
    hover = HoverTool(
        tooltips=[
            ("Date", '@date{%Y-%m-%d %H:%M:%S}'),
            ("Open", '@open{0.00000 a}'), ("High", '@high{0.00000 a}'),
            ("Low", "@low{0.00000 a}"), ("Close", "@close{0.00000 a}")],
        formatters={'@date': 'datetime'}, mode='vline', renderers=[render])
    
    dashboard.add_tools(hover)

    #############################################################################################################################################################

    upper_cols = [col for col in subopanel_ti.columns if sub_order[0] in col]
    lower_cols = [col for col in subopanel_ti.columns if sub_order[1] in col]

    upper_sub, lower_sub = subopanel_ti[upper_cols], subopanel_ti[lower_cols]

    source_rgb, source_avgr = ColumnDataSource(data=upper_sub), ColumnDataSource(data=lower_sub)

    p_rgb: figure = figure(tools='reset, pan, ywheel_zoom', x_axis_type="datetime", width=1750, height=200, y_axis_location="right", 
                           background_fill_color = 'black', toolbar_location='right', x_range=dashboard.x_range, active_drag='pan', ) # output_backend="webgl"
    
    crosshair = CrosshairTool(line_color="white")  # puedes usar hex o nombres de color
    p_rgb.add_tools(crosshair)

    p_avgr: figure = figure(tools='reset, pan, ywheel_zoom', x_axis_type="datetime", width=1750, height=200, y_axis_location="right",
                             background_fill_color = 'black', toolbar_location='right', x_range=dashboard.x_range, active_drag='pan', ) # output_backend="webgl"
    
    crosshair = CrosshairTool(line_color="white")  # puedes usar hex o nombres de color
    p_avgr.add_tools(crosshair)

    p_rgb.xaxis.visible = False
    p_rgb.grid.grid_line_color = 'black'
    p_avgr.grid.grid_line_color = 'black'

    p_avgr.xaxis.major_label_overrides = {i: date.strftime('%d/%m/%Y  %H:%M:%S') for i, date in enumerate(df["date"])}

    render_rgb = p_rgb.line(x="index", y="rsi", line_color="orange", line_width=1.5, source=source_rgb)
    p_rgb.line(x="index", y="rsi_ma", line_color="white", line_width=1.5, source=source_rgb)
    
    render_avgr = p_avgr.line(x="index", y="atr", line_color="white", line_width=1.5, source=source_avgr)
    # p_avgr.line(x="index", y="avgrn", line_color="white", line_width=1.5, source=source_avgr)
    
    hover_lines_rgb = HoverTool(
        tooltips=[("date", '@date{%Y-%m-%d %H:%M:%S}'),
                  ("rgbp", "@rgbp"),
                  ("rgbn", "@rgbn")],
        formatters={"@date": "datetime"},
        mode="vline",
        renderers=[render_rgb])

    hover_lines_avgr = HoverTool(
        tooltips=[("date", '@date{%Y-%m-%d %H:%M:%S}'),
                  ("avgrp", "@avgrp"),
                  ("avgrn", "@avgrn")],
        formatters={"@date": "datetime"},
        mode="vline",
        renderers=[render_avgr])

    p_rgb.add_tools(hover_lines_rgb), p_avgr.add_tools(hover_lines_avgr)
    
    return dashboard, source_candle, source_over, p_rgb, source_rgb, p_avgr, source_avgr
