from graph.backtesting_component import net_value_line, returns_distribution, entry_exit_dot, entrust_dot
from plotly import graph_objects as go
from graph.bar_component import ohlc, candlestick
import plotly.figure_factory as ff
import plotly.express as px
import numpy as np

import calendar

from graph.indicator_component import macd_graph, sar_graph

calendar.setfirstweekday(calendar.SUNDAY)
import pandas as pd
import plotly.io as pio
from plotly.subplots import make_subplots

from technical_analysis.momentum import *
from technical_analysis.pattern import *
from technical_analysis.volume import *
from technical_analysis.volatility import *
from technical_analysis.overlap import *
from technical_analysis.statistic_function import *
from technical_analysis.customization import *

pio.renderers.default = "browser"


def net_value_plot(strategy_net_value: pd.Series,
                   benchmark: pd.Series or None = None,
                   strategy_name='strategy', fill=None):
    fig = go.Figure()
    fig.add_trace(net_value_line(strategy_net_value / strategy_net_value[0], name=strategy_name, fill=fill))
    if benchmark is not None:
        benchmark_copy = benchmark[
            (benchmark.index >= strategy_net_value.index[0]) & (benchmark.index <= strategy_net_value.index[-1])]
        fig.add_trace(net_value_line(benchmark_copy / benchmark_copy[0], color='#FFCC00', name='benchmark'))

    x_axis = fig.data[0].x
    tick_value = [x_axis[i] for i in range(0, len(x_axis), len(x_axis) // 5)]
    tick_text = [x_axis[i][0:10] for i in range(0, len(x_axis), len(x_axis) // 5)]
    fig.update_xaxes(ticktext=tick_text, tickvals=tick_value)

    return fig


def returns_distribution_plot(returns: pd.Series):
    fig = go.Figure()
    fig.add_trace(returns_distribution(returns))
    fig.update_layout(
        title="Return Distribution", )
    return fig


def ret_verus_ret(rets: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=rets['close'], y=rets['equity'], mode='markers'))
    fig.update_xaxes(title_text="benchmark returns")
    fig.update_yaxes(title_text="strategy returns")
    return fig


def entry_and_exit_plot(ohlc_df, traded: pd.DataFrame, symbol: str, ohlc_graph=True, price_key='close', ohlc_key=None,
                        entrust=False, ta_dict: None or dict = None):
    # traded columns:
    # code,order_time,order_price,order_qty,order_type,dealt_price,dealt_qty,order_direction,order_status,update_time,
    # exchange_order_id,order_id,cash_inflow
    subplot_num = 1
    if ta_dict is not None:
        subplot_num += len([i for i in ta_dict.values() if i is False])

    row_heights = [1] * subplot_num
    row_heights[0] = 2

    fig = make_subplots(
        rows=subplot_num, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03, row_heights=row_heights
    )
    # filter out unrelated trade
    traded = traded[traded['code'] == symbol]
    long = traded[traded['order_direction'] == 'LONG']
    short = traded[traded['order_direction'] == 'SHORT']

    if ohlc_graph:
        candles = candlestick(ohlc_df, ohlc_key=ohlc_key, symbol=symbol)
        fig.add_trace(candles, 1, 1)
    else:
        prices = net_value_line(ohlc_df[price_key], color='#FFA500', name=symbol)
        fig.add_trace(prices, 1, 1)

    long_dot = entry_exit_dot(long, True)
    short_dot = entry_exit_dot(short, False)
    fig.add_trace(long_dot, 1, 1)
    fig.add_trace(short_dot, 1, 1)
    if entrust:
        entrust_long = entrust_dot(long, True)
        entrust_short = entrust_dot(short, False)
        fig.add_trace(entrust_long, 1, 1)
        fig.add_trace(entrust_short, 1, 1)

    if ta_dict is not None:
        subplot_i = 2
        for ta, overlap in ta_dict.items():
            call_str = ta.replace('inputs', 'ohlc_df')
            ta_indicator = eval(call_str)
            ta_name = call_str.split('(')[0]
            if isinstance(ta_indicator, pd.Series):
                index = ta_indicator.index.strftime('%Y/%m/%d %H:%M:%S')
                if overlap is True:
                    if ta_name == 'SAR':
                        fig.add_trace(sar_graph(ta_indicator, ohlc_df['close']), 1, 1)
                    else:
                        fig.add_trace(go.Scatter(x=index, y=ta_indicator, mode='lines', name=call_str), 1, 1)
                else:
                    fig.add_trace(go.Scatter(x=index, y=ta_indicator, mode='lines', name=call_str), subplot_i, 1)
                    subplot_i += 1
            elif isinstance(ta_indicator, pd.DataFrame):
                index = ta_indicator.index.strftime('%Y/%m/%d %H:%M:%S')

                if overlap is True:
                    for col in ta_indicator.columns:
                        fig.add_trace(go.Scatter(x=index, y=ta_indicator[col], mode='lines', name=col), 1, 1)
                else:
                    if ta_name == 'MACD' or ta_name == 'MACDEXT' or ta_name == 'MACDFIX':
                        fig.add_traces(macd_graph(ta_indicator), [subplot_i] * 3, [1] * 3)
                    else:
                        for col in ta_indicator.columns:
                            fig.add_trace(go.Scatter(x=index, y=ta_indicator[col], mode='lines', name=col), subplot_i,
                                          1)
                    subplot_i += 1

    x_axis = fig.data[0].x
    tick_value = [x_axis[i] for i in range(0, len(x_axis), len(x_axis) // 5)]
    tick_text = [x_axis[i][0:10] for i in range(0, len(x_axis), len(x_axis) // 5)]
    fig.update_xaxes(ticktext=tick_text, tickvals=tick_value)
    # fig.update_layout(showlegend=True, xaxis_rangeslider_visible=False)
    fig.update_layout(showlegend=True, height=175 * len(fig.data),
                      yaxis1=dict(autorange=True, fixedrange=False),
                      yaxis2=dict(autorange=True, fixedrange=False),
                      xaxis_rangeslider_visible=False, hovermode='x unified'
                      )
    return fig


def maximum_drawdown_plot(drawdown_percent: pd.Series):
    fig = go.Figure()
    fig.add_trace(net_value_line(drawdown_percent, color='#73B839', name='underwater', fill='tozeroy'), )
    fig.update_layout(
        title="Underwater", )
    x_axis = fig.data[0].x
    tick_value = [x_axis[i] for i in range(0, len(x_axis), len(x_axis) // 5)]
    tick_text = [x_axis[i][0:10] for i in range(0, len(x_axis), len(x_axis) // 5)]
    fig.update_xaxes(ticktext=tick_text, tickvals=tick_value)
    return fig


def daily_heatmap(agg_ret: pd.Series) -> go.Figure:
    num_of_months = len(agg_ret.index.to_period('M').unique())
    num_of_rows = (num_of_months // 3) + 1 if num_of_months % 3 != 0 else (num_of_months // 3)
    fig = make_subplots(rows=num_of_rows, cols=3,
                        # shared_xaxes=True,
                        subplot_titles=agg_ret.index.to_period('M').unique().to_native_types(),
                        vertical_spacing=0.1,
                        horizontal_spacing=0.01
                        )
    row = 1
    col = 1
    agg_ret_ = agg_ret.copy().replace(0, np.NAN)
    agg_ret_ = (agg_ret_ - agg_ret_.min()) / (agg_ret_.max() - agg_ret_.min())

    for g in agg_ret_.groupby(pd.Grouper(freq='M')):
        x = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
        cal = calendar.monthcalendar(g[0].year, g[0].month)
        y = ['Week ' + str(i) for i in range(1, len(cal) + 1)]
        # data g[1]
        z = []
        z_text = []
        i = 0
        # print(g)
        for week in cal:
            wl = []
            wl_text = []
            for wd in week:
                if i == len(g[1]):
                    wl.append(np.NAN)
                    wl_text.append('')
                elif wd == 0:
                    wl.append(np.NAN)
                    wl_text.append('')
                elif g[1].index[i].day == wd:
                    wl.append(g[1][i])
                    wl_text.append('{:.3f} %'.format(100 * agg_ret[i]))
                    i += 1
                else:
                    wl.append(np.NAN)
                    wl_text.append('')

            z.append(wl)
            z_text.append(wl_text)
        colorscale = [[0, 'red'], [0.5, 'yellow'], [1, 'green']]
        # todo Annotations
        fig1 = go.Heatmap(z=z, x=x, y=y,
                          colorscale=colorscale,
                          # xgap=3,  # this
                          # ygap=3,  # and this is used to make the grid-like apperance
                          # text=z_text,
                          hovertext=z_text,
                          hoverinfo='x+y+text',
                          showscale=False,
                          )

        fig.add_trace(fig1, row=row, col=col)
        # print(row, col)
        if col == 3:
            row += 1
            col = 0
        col = (col + 1) % 4

    layout = dict(plot_bgcolor='#fff', width=700, height=700, )
    for i in range(1, num_of_months + 1):
        if i % 3 == 1:
            layout['yaxis' + str(i)] = dict(
                showline=False, showgrid=False, zeroline=False, autorange="reversed"
            )
        else:
            layout['yaxis' + str(i)] = dict(
                showline=False, showgrid=False, zeroline=False, visible=False, autorange="reversed"
            )
        if i >= num_of_months - 2:
            layout['xaxis' + str(i)] = dict(showline=False, showgrid=False, zeroline=False)
        else:
            layout['xaxis' + str(i)] = dict(showline=False, showgrid=False, zeroline=False, visible=False)

    fig.update_layout(
        layout
    )

    return fig


def weekly_heatmap(agg_ret: pd.Series) -> go.Figure:
    fig = go.Figure()
    # num_of_months = len(agg_ret.index.to_period('M').unique())

    agg_ret_ = agg_ret.copy().replace(0, np.NAN)
    agg_ret_ = (agg_ret_ - agg_ret_.min()) / (agg_ret_.max() - agg_ret_.min())
    y = agg_ret_.index.to_period('M').unique().strftime('%Y-%m')

    # for
    # cal = calendar.monthcalendar(g[0].year, g[0].month)
    x = ['Week ' + str(i) for i in range(1, 6)]
    z = []
    z_text = []
    i = 0
    for month in y:
        z1 = []
        z1_text = []
        for w in x:
            if i < len(agg_ret_) and agg_ret_.index[i].strftime('%Y-%m') == month:
                z1.append(agg_ret_[i])
                z1_text.append('{:.3f} %'.format(100 * agg_ret[i]))
                i += 1
            else:
                z1.append(None)
                z1_text.append(None)
        z.append(z1)
        z_text.append(z1_text)
    colorscale = [[0, 'red'], [0.5, 'yellow'], [1, 'green']]
    # todo Annotations
    heatmap = go.Heatmap(z=z, x=x, y=y,
                         colorscale=colorscale,
                         # xgap=3,  # this
                         # ygap=3,  # and this is used to make the grid-like apperance
                         # text=z_text,
                         hovertext=z_text,
                         hoverinfo='x+y+text',
                         showscale=False,
                         )
    layout = dict(plot_bgcolor='#fff', width=700, height=700, )
    layout['yaxis'] = dict(
        showline=False, showgrid=False, zeroline=False, autorange="reversed"
    )
    layout['xaxis'] = dict(
        showline=False, showgrid=False, zeroline=False)
    fig.add_trace(heatmap)
    fig.update_layout(layout)
    return fig


def monthly_heatmap(agg_ret: pd.Series) -> go.Figure:
    fig = go.Figure()

    agg_ret_ = agg_ret.copy().replace(0, np.NAN)
    agg_ret_ = (agg_ret_ - agg_ret_.min()) / (agg_ret_.max() - agg_ret_.min())
    y = agg_ret_.index.to_period('Y').unique().strftime('%Y').to_list()

    # for
    # cal = calendar.monthcalendar(g[0].year, g[0].month)
    x = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    z = []
    z_text = []
    i = 0
    for y_ in y:
        z1 = []
        z1_text = []
        for w in x:
            if i < len(agg_ret_) and agg_ret_.index[i].month - 1 == len(z1):
                z1.append(agg_ret_[i])
                z1_text.append('{:.3f} %'.format(100 * agg_ret[i]))
                i += 1
            else:
                z1.append(None)
                z1_text.append(None)
        z.append(z1)
        z_text.append(z1_text)
    colorscale = [[0, 'red'], [0.5, 'yellow'], [1, 'green']]
    # todo Annotations
    heatmap = go.Heatmap(z=z, x=x, y=y,
                         colorscale=colorscale,
                         # xgap=3,  # this
                         # ygap=3,  # and this is used to make the grid-like apperance
                         # text=z_text,
                         hovertext=z_text,
                         hoverinfo='x+y+text',
                         showscale=False,
                         )
    layout = dict(plot_bgcolor='#fff', width=700, height=700, )
    layout['yaxis'] = dict(
        showline=False, showgrid=False, zeroline=False, autorange="reversed", type='category'
    )
    layout['xaxis'] = dict(
        showline=False, showgrid=False, zeroline=False)
    fig.add_trace(heatmap)
    fig.update_layout(layout)
    return fig


def quarter_heatmap(agg_ret: pd.Series) -> go.Figure:
    fig = go.Figure()

    agg_ret_ = agg_ret.copy().replace(0, np.NAN)
    agg_ret_ = (agg_ret_ - agg_ret_.min()) / (agg_ret_.max() - agg_ret_.min())
    y = agg_ret_.index.to_period('Y').unique().strftime('%Y').to_list()

    x = ['Q1', 'Q2', 'Q3', 'Q4']
    z = []
    z_text = []
    i = 0
    for y_ in y:
        z1 = []
        z1_text = []
        for w in x:
            if i < len(agg_ret_) and agg_ret_.index[i].quarter - 1 == len(z1):
                z1.append(agg_ret_[i])
                z1_text.append('{:.3f} %'.format(100 * agg_ret[i]))
                i += 1
            else:
                z1.append(None)
                z1_text.append(None)
        z.append(z1)
        z_text.append(z1_text)
    colorscale = [[0, 'red'], [0.5, 'yellow'], [1, 'green']]
    # todo Annotations
    heatmap = go.Heatmap(z=z, x=x, y=y,
                         colorscale=colorscale,
                         # xgap=3,  # this
                         # ygap=3,  # and this is used to make the grid-like apperance
                         # text=z_text,
                         hovertext=z_text,
                         hoverinfo='x+y+text',
                         showscale=False,
                         )
    layout = dict(plot_bgcolor=('#fff'))
    layout['yaxis'] = dict(
        showline=False, showgrid=False, zeroline=False, autorange="reversed", type='category'
    )
    layout['xaxis'] = dict(
        showline=False, showgrid=False, zeroline=False)
    fig.add_trace(heatmap)
    fig.update_layout(layout)
    return fig


def year_heatmap(agg_ret: pd.Series) -> go.Figure:
    """

    :param agg_ret:
    :return:
    """
    fig = go.Figure()
    agg_ret_ = agg_ret.copy().replace(0, np.NAN)
    agg_ret_ = (agg_ret_ - agg_ret_.min()) / (agg_ret_.max() - agg_ret_.min())
    y = agg_ret_.index.to_period('Y').unique().strftime('%Y').to_list()
    years = [i for i in range(5 * int(int(y[0]) / 5), int((int(y[-1]) + 5) / 5) * 5, 1)]
    z = []
    z_text = []
    x = []
    j = 0
    decade = 1
    z1 = []
    z1_text = []
    for i in range(len(years)):
        if j < len(y) and int(y[j]) == years[i]:
            z1.append(agg_ret_[j])
            z1_text.append('{:.3f} %'.format(100 * agg_ret[j]))
            j += 1
        else:
            z1.append(None)
            z1_text.append(None)
        if i % 5 == 4:
            z.append(z1)
            z_text.append(z1_text)
            z1 = []
            x.append(decade)
            decade += 1

    colorscale = [[0, 'red'], [0.5, 'yellow'], [1, 'green']]
    # todo Annotations
    heatmap = go.Heatmap(z=z, y=x, x=y,
                         colorscale=colorscale,
                         # xgap=3,  # this
                         # ygap=3,  # and this is used to make the grid-like apperance
                         # text=z_text,
                         hovertext=z_text,
                         hoverinfo='x+y+text',
                         showscale=False,
                         )
    layout = dict(plot_bgcolor='#fff')
    layout['yaxis'] = dict(
        showline=False, showgrid=False, zeroline=False, autorange="reversed", type='category'
    )
    layout['xaxis'] = dict(
        showline=False, showgrid=False, zeroline=False)
    fig.add_trace(heatmap)
    fig.update_layout(layout)
    return fig


def aggregate_returns_heatmap(agg_ret: pd.Series, period):
    if period == 'day':
        return daily_heatmap(agg_ret)
    elif period == 'week':
        return weekly_heatmap(agg_ret)
    elif period == 'month':
        return monthly_heatmap(agg_ret)
    elif period == 'quarter':
        return quarter_heatmap(agg_ret)
    elif period == 'year':
        return year_heatmap(agg_ret)
