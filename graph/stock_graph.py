import plotly.graph_objects as go
import numpy as np
import pandas as pd
from plotly.subplots import make_subplots
import datetime


def _set_xlabel(index):
    intraday = False
    start_datetime = datetime.datetime.strptime(index[0], '%Y/%m/%d %H:%M:%S')
    end_datetime = datetime.datetime.strptime(index[-1], '%Y/%m/%d %H:%M:%S')
    interval = datetime.datetime.strptime(index[1], '%Y/%m/%d %H:%M:%S') - start_datetime
    interval = interval.seconds / 60
    if interval < 30:
        interval = 30
    if start_datetime.date() == end_datetime.date():
        intraday = True

    values = [index[0]]
    texts = []
    if intraday:
        texts.append(index[0].split(' ')[0])
        for i in range(1, len(index) // interval):
            values.append(index[i * interval])
            texts.append(index[i * interval].split(' ')[1])
        if values[-1] != index[-1]:
            values.append(index[len(index) - 1])
            texts.append(index[len(index) - 1].split(' ')[1])
    else:

        day = start_datetime
        texts.append(index[0].split(' ')[0])
        i = 1
        interval = interval / (60 * 24)
        while day < end_datetime:
            values.append(index[i * interval])
            texts.append(index[i * interval])
            day += datetime.timedelta(days=1)
            i += 1

        if values[-1] != index[-1]:
            values.append(index[len(index) - 1])
            texts.append(index[len(index) - 1].split(' ')[1])

    return texts, values


def stick_and_volume(bar_component, volume_component, type='intraday'):
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        specs=[[{"type": "xy"}],
               [{"type": "bar"}]]
    )
    fig.add_trace(bar_component, row=1, col=1)
    fig.add_trace(volume_component, row=2, col=1)
    time = bar_component.x
    text, vals = _set_xlabel(time)
    fig.update_xaxes(
        ticktext=text,
        tickvals=vals
    )
    return fig


def stick_overlap_indicator(bar_component, overlap):
    data = [bar_component]
    data.extend(list(overlap))

    fig = go.Figure(data)
    time = bar_component.x
    text, vals = _set_xlabel(time)
    fig.update_xaxes(
        ticktext=text,
        tickvals=vals
    )
    return fig


def stick_and_nonoverlap_indicators(bar_component, indicators, type='intraday'):
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        specs=[[{"type": "xy"}],
               [{"type": "xy"}]]
    )
    fig.add_trace(bar_component, row=1, col=1)
    for indicator in indicators:
        fig.add_trace(indicator, row=2, col=1)
    time = bar_component.x
    text, vals = _set_xlabel(time)
    fig.update_xaxes(
        ticktext=text,
        tickvals=vals
    )
    # go.update
    return fig


def stick_and_indicators(bar_component, indicators, rows):
    fig = make_subplots(
        rows=max(rows) + 1, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        # specs=[[{"type": "xy"}],
        #        [{"type": "xy"}]]
    )
    fig.add_trace(bar_component, row=1, col=1)
    i = 0
    for indicator in indicators:
        fig.add_trace(indicator, row=rows[i] + 1, col=1)
        i += 1
    time = bar_component.x
    text, vals = _set_xlabel(time)
    fig.update_xaxes(
        ticktext=text,
        tickvals=vals
    )
    # go.update
    return fig
