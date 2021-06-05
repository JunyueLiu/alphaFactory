# This is for chart study
# 1. have more intuitive observation of technical indicator and chart pattern
# 2. fast and direct testing the indicator in simple way
from datetime import timedelta
from typing import Dict, Optional, List, Union
import inspect

import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.validators.scatter.marker import SymbolValidator

from graph import purple
from graph.bar_component import candlestick
from graph.indicator_component import sar_graph, rsi_graph, macd_graph, channel_graph
from technical_analysis.momentum import *
from technical_analysis.opt import pivotlow, pivothigh
from technical_analysis.pattern import *
from technical_analysis.volume import *
from technical_analysis.volatility import *
from technical_analysis.overlap import *
from technical_analysis.statistic_function import *
from technical_analysis.customization import *
from technical_analysis.channel import *
from technical_analysis import channel

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


class ChartVisualizer:
    def __init__(self, ohlc: pd.DataFrame, ta_dict: Dict, widget_dict: Optional[Dict] = None,
                 ohlc_key: Optional[List] = None, default_bars_num=500):
        self.ohlc = ohlc
        self.ta_dict = ta_dict
        self.ohlc_key = ohlc_key
        self.widget_dict = widget_dict
        self.default_bars_num = default_bars_num
        self.app = \
            dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)
        self.ta = self._cal_ta()
        self.widget = self._get_widget()

    def _cal_ta(self) -> Dict[str, Union[pd.DataFrame, pd.Series]]:
        ta = {}
        for name, setting in self.ta_dict.items():
            paras = {k: v for k, v in setting.items()
                     if k in inspect.getfullargspec(eval(setting['indicator'])).args}
            ta[name] = eval('{}(self.ohlc, **paras)'.format(setting['indicator']))
        return ta

    def _get_widget(self):
        widget = {}
        if self.widget_dict:
            for name, setting in self.widget_dict.items():
                chart_type = setting.get('type')
                target_ta = setting.get('target_ta')
                if chart_type == 'breakthrough':
                    band = setting.get('band')
                    direction = setting.get('direction', 1)
                    y = setting.get('y')  # type: str
                    ta = self.ta[target_ta][band].shift(1)
                    if direction == 1:
                        price = self.ohlc['high']
                        idx = ta[price >= ta].index
                    else:
                        price = self.ohlc['low']
                        idx = ta[price <= ta].index
                    if 'band' in y:
                        multiple = y.replace('band', '').replace('*', '').strip()
                        multiple = 1 if len(multiple) == 0 else float(multiple)
                        w = pd.Series((multiple * ta)[idx], index=idx, name=name)
                        widget[name] = w
                    elif 'close' in y:
                        multiple = y.replace('close', '').replace('*', '').strip()
                        multiple = 1 if len(multiple) == 0 else float(multiple)
                        w = pd.Series((multiple * self.ohlc['close'])[idx], index=idx, name=name)
                        widget[name] = w
                    else:
                        raise NotImplementedError
                elif chart_type == 'pivot':
                    pivot_para = setting.get('pivot_para', {'bar_left': 3, 'bar_right': 5, 'type': 'high'})
                    filter_ = pivot_para.get('filter')
                    ta = self.ta[target_ta]
                    if pivot_para['type'] == 'low':
                        pv = pivotlow(ta, pivot_para['bar_left'], pivot_para['bar_right'])
                    else:
                        pv = pivothigh(ta, pivot_para['bar_left'], pivot_para['bar_right'])
                    pv = pv.dropna()
                    if filter_:
                        if 'min' in filter_:
                            idx = ta[ta >= filter_['min']].index
                            pv = pv[pv.index.intersection(idx)]
                        if 'max' in filter_:
                            idx = ta[ta <= filter_['max']].index
                            pv = pv[pv.index.intersection(idx)]
                    widget[name] = pv
                elif chart_type == 'support':
                    support_paras = setting.get('support_para')
                    y = setting.get('y')  # type: str
                    if y in ['open', 'close', 'low', 'high']:
                        prices = self.ohlc[y]
                    elif y == 'ohlc4':
                        prices = (self.ohlc['open'] + self.ohlc['high'] +
                                  self.ohlc['low'] + self.ohlc['low']) / 4
                    else:
                        raise NotImplementedError
                    if support_paras['type'] == 'pivot':
                        if target_ta is None:
                            series = prices
                        else:
                            series = self.ta[target_ta]
                        pv = pivotlow(series, support_paras['para']['bar_left'],
                                      support_paras['para']['bar_right'])
                        pv = pv.dropna()
                        filter_ = support_paras['para'].get('filter')
                        if filter_:
                            if 'min' in filter_:
                                idx = series[series >= filter_['min']].index
                                pv = pv[pv.index.intersection(idx)]
                            if 'max' in filter_:
                                idx = series[series <= filter_['max']].index
                                pv = pv[pv.index.intersection(idx)]
                        support = prices[prices.index.intersection(pv.index)] \
                            .reindex(self.ohlc.index).fillna(method='ffill')
                        widget[name] = support
                    else:
                        raise NotImplementedError
                elif chart_type == 'resistance':
                    resistance_paras = setting.get('resistance_para')
                    y = setting.get('y')  # type: str
                    if y in ['open', 'close', 'low', 'high']:
                        prices = self.ohlc[y]
                    elif y == 'ohlc4':
                        prices = (self.ohlc['open'] + self.ohlc['high'] +
                                  self.ohlc['low'] + self.ohlc['low']) / 4
                    else:
                        raise NotImplementedError
                    if resistance_paras['type'] == 'pivot':
                        if target_ta is None:
                            series = prices
                        else:
                            series = self.ta[target_ta]
                        pv = pivothigh(series, resistance_paras['para']['bar_left'],
                                       resistance_paras['para']['bar_right'])
                        pv = pv.dropna()
                        filter_ = resistance_paras['para'].get('filter')
                        if filter_:
                            if 'min' in filter_:
                                idx = series[series >= filter_['min']].index
                                pv = pv[pv.index.intersection(idx)]
                            if 'max' in filter_:
                                idx = series[series <= filter_['max']].index
                                pv = pv[pv.index.intersection(idx)]
                        resistance = prices[prices.index.intersection(pv.index)] \
                            .reindex(self.ohlc.index).fillna(method='ffill')
                        widget[name] = resistance
                    else:
                        raise NotImplementedError
                elif chart_type == 'zone':
                    condition = setting.get('condition')  # type: str
                    if isinstance(target_ta, list):
                        for t in target_ta:
                            condition = condition.replace(t, "self.ta['{}']".format(t))
                    else:
                        condition = condition.replace(target_ta, "self.ta['{}']".format(target_ta))
                    s = pd.Series(np.where(eval(condition), 1, 0), index=self.ohlc.index)

                    s_shift = s.shift(1)
                    start_idx = s[(s == 1) & (s_shift == 0)].index
                    end_idx = s[((s == 0) & (s_shift == 1)).shift(-1) == True].index.values
                    s = pd.Series(end_idx, index=start_idx, name=name)
                    widget[name] = s
                elif chart_type == 'box':
                    # todo box, such as atr box for entry point...
                    pass
                elif chart_type == 'trendline':
                    pass

                else:
                    raise NotImplementedError

        return widget

    def _get_chart(self, start=None, end=None) -> go.Figure:

        subplot_num = 1
        subplot_num += len([para for para in self.ta_dict.values()
                            if 'overlap' in para and para['overlap'] is False])

        row_heights = [1] * subplot_num
        row_heights[0] = 2

        fig = make_subplots(
            rows=subplot_num, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.03,
            row_heights=row_heights
        )

        try:
            symbol = self.ohlc['code'][0]
        except:
            symbol = None

        data = self.ohlc.copy()
        if start is not None:
            start = pd.to_datetime(start)
            data = data.loc[start:]

        if end is not None:
            end = pd.to_datetime(end)
            data = data.loc[:end]

        candles = candlestick(data, ohlc_key=self.ohlc_key, symbol=symbol)
        fig.add_trace(candles, 1, 1)
        subplot_i = 2
        for name, setting in self.ta_dict.items():
            ta_indicator = self.ta[name]
            if start is not None:
                ta_indicator = ta_indicator.loc[start:]

            if end is not None:
                ta_indicator = ta_indicator.loc[:end]

            ta_name = setting['indicator']
            overlap = setting.get('overlap')
            color = setting.get('color')
            if isinstance(ta_indicator, pd.Series):
                index = ta_indicator.index.strftime('%Y/%m/%d %H:%M:%S')
                if overlap is None:
                    continue
                elif overlap is True:
                    if ta_name == 'SAR':
                        fig.add_trace(sar_graph(ta_indicator, data['close']), 1, 1)
                    else:
                        fig.add_trace(go.Scatter(x=index, y=ta_indicator, mode='lines', name=name,
                                                 line_color=color), 1, 1)
                else:
                    if ta_name == 'RSI':
                        fig.add_traces(rsi_graph(ta_indicator).data, subplot_i, 1)
                    else:
                        fig.add_trace(go.Scatter(x=index,
                                                 y=ta_indicator,
                                                 mode='lines',
                                                 name=name, line_color=color), subplot_i, 1)
                    subplot_i += 1
            elif isinstance(ta_indicator, pd.DataFrame):
                index = ta_indicator.index.strftime('%Y/%m/%d %H:%M:%S')
                if overlap is None:
                    continue
                elif overlap is True:
                    i = 0
                    if ta_name in channel.__func__:
                        fig.add_traces(list(channel_graph(ta_indicator)), 1, 1)
                    else:
                        for col in ta_indicator.columns:
                            fig.add_trace(go.Scatter(x=index, y=ta_indicator[col],
                                                     mode='lines', name=col, line_color=color[i]), 1, 1)
                            i += 1
                else:
                    if ta_name in ['MACD', 'MACDEXT', 'MACDFIX']:
                        fig.add_traces(macd_graph(ta_indicator), [subplot_i] * 3, [1] * 3)
                    else:
                        i = 0
                        for col in ta_indicator.columns:
                            fig.add_trace(
                                go.Scatter(x=index, y=ta_indicator[col],
                                           mode='lines', name=col, line_color=color[i]), subplot_i, 1)
                            i += 1
                    subplot_i += 1

        if self.widget_dict is not None:
            for name, setting in self.widget_dict.items():
                widget = self.widget[name]
                # if start is not None:
                #     widget = widget.loc[start:]
                #
                # if end is not None:
                #     widget = widget.loc[:end]

                subplot = setting.get('subplot')
                marker = setting.get('marker', None)
                line = setting.get('line', None)

                if setting.get('type') == 'zone':
                    fillcolor = setting.get('fillcolor', 'lightblue')
                    for s, e in widget.items():
                        if e < start or s > end:
                            continue

                        if s < start <= e:
                            s = start
                        if e > end:
                            e = end

                        fig.add_vrect(x0=s.strftime('%Y/%m/%d %H:%M:%S'),
                                      x1=e.strftime('%Y/%m/%d %H:%M:%S'),
                                      y0=data['low'].min(),
                                      y1=data['high'].max(),
                                      # row=1, col=1,
                                      # annotation_text=name,
                                      # annotation_position="top left",
                                      fillcolor=fillcolor, opacity=0.1, line_width=0)
                else:
                    if start is not None:
                        widget = widget.loc[start:]

                    if end is not None:
                        widget = widget.loc[:end]

                    index = widget.index.strftime('%Y/%m/%d %H:%M:%S')
                    if isinstance(widget, pd.Series):
                        if marker:
                            fig.add_trace(go.Scatter(x=index, y=widget, mode='markers', name=name,
                                                     marker=marker), subplot, 1)
                        elif line:
                            fig.add_trace(go.Scatter(x=index, y=widget, mode='lines', name=name,
                                                     line=line), subplot, 1)
                    elif isinstance(widget, pd.DataFrame):
                        raise NotImplementedError

        x_axis = fig.data[0].x
        tick_value = [x_axis[i] for i in range(0, len(x_axis), len(x_axis) // 5)]
        tick_text = [x_axis[i][0:10] for i in range(0, len(x_axis), len(x_axis) // 5)]
        fig.update_xaxes(ticktext=tick_text, tickvals=tick_value)
        fig.update_layout(showlegend=True,
                          yaxis1=dict(autorange=True, fixedrange=False),
                          yaxis2=dict(autorange=True, fixedrange=False),
                          xaxis_rangeslider_visible=False, hovermode='x unified',
                          template='plotly_white'
                          )

        return fig

    def get_app(self):

        min_date = self.ohlc.index[0]
        max_date = self.ohlc.index[-1]
        start_date = self.ohlc.index[-self.default_bars_num]
        self.app.layout = html.Div([
            dcc.DatePickerRange(
                id='date-picker-range',
                min_date_allowed=min_date,
                max_date_allowed=max_date,
                initial_visible_month=max_date,
                start_date=start_date,
                end_date=max_date
            ),
            dcc.Input(
                type='number',
                id='input',
                value=self.default_bars_num,
                min=0, step=100,

            ),
            html.Button(
                children='Previous',
                id='previous'
            ),
            html.Button(
                children='Next',
                id='next'
            ),

            html.Button(
                children='Submit',
                id='submit'
            ),
            html.Button(
                children='Save',
                id='save-image'
            ),

            dcc.Graph(
                id='main-candle'
                , config={'autosizable': True, 'fillFrame': True}
            ), ],
            # style={
            #     'height': '2000',
            #     # 'float': 'left'
            # }

        )

        @self.app.callback(
            [Output('main-candle', 'figure'),
             Output('date-picker-range', 'start_date'),
             Output('date-picker-range', 'end_date'),

             ],
            [
                Input('submit', 'n_clicks'),
                Input('previous', 'n_clicks'),
                Input('next', 'n_clicks')],
            [
                State('date-picker-range', 'start_date'),
                State('date-picker-range', 'end_date'),
                State('input', 'value'),
            ])
        def update_main_candle(submit_clicks,
                               previous_clicks,
                               next_clicks, start_date, end_date, input_value):
            changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
            if 'submit' in changed_id:
                fig = self._get_chart(start=start_date, end=end_date)
            elif 'previous' in changed_id:
                end_date = start_date
                start_date = self.ohlc.loc[:start_date].index[-input_value:][0]
                if start_date == min_date:
                    start_date = min_date
                    end_date = self.ohlc.index[self.default_bars_num]
                fig = self._get_chart(start=start_date, end=end_date)
            elif 'next' in changed_id:
                start_date = end_date
                end_date = self.ohlc.loc[end_date:].index[:input_value][-1]
                if end_date == max_date:
                    start_date = self.ohlc.index[-self.default_bars_num]
                    end_date = max_date
                fig = self._get_chart(start=start_date, end=end_date)
            else:
                fig = self._get_chart(start=start_date, end=end_date)

            return fig, start_date, end_date

        return self.app


if __name__ == '__main__':
    ohlc_df = pd.read_csv('../../local_data/EURUSD/count5000.csv')
    ohlc_df['date'] = pd.to_datetime(ohlc_df['date'])
    ohlc_df.set_index('date', inplace=True)
    ohlc_df = ohlc_df.loc[pd.to_datetime('2020/01/01'):]

    ta_paras = {
        "MA1": {
            "indicator": "DEMA",
            "period": 60,
            "overlap": True,
            "color": "lightblue"
        },
        "MA2": {
            "indicator": "DEMA",
            "period": 120,
            "overlap": True,
            "color": "midnightblue"
        },
        "MA3": {
            "indicator": "DEMA",
            "period": 240,
            "overlap": True,
            "color": "blue"
        },
        "BD": {
            "indicator": "Bollinger_Donchian",
            # "period": 20,
            "overlap": True,

        },

        "MACD": {
            "indicator": "MACD",
            "overlap": False
        },
        "RSI": {
            "indicator": "RSI",
            "overlap": False
        },

    }

    widget_paras = {
        "up_channal": {
            "type": "breakthrough",
            "target_ta": "BD",
            "band": "upperband",
            "direction": 1,
            "y": "band",
            "subplot": 1,
            "marker": {
                "symbol": "triangle-up",
                "color": "green",
                "size": 15
            },
        },
        "rsi_oversold": {
            'target_ta': 'RSI',
            "type": "pivot",
            "y": "value",
            "subplot": 3,
            "marker": {
                "symbol": "circle-open",
                "color": "red",
                "size": 15
            },
            'pivot_para': {
                'type': 'low',
                'filter': {
                    'min': 0,
                    'max': 40,
                },
                'bar_left': 3,
                'bar_right': 3,
            },

        },
        "rsi_support": {
            'target_ta': 'RSI',
            "type": "support",
            "y": "close",
            "subplot": 1,
            "marker": {
                "symbol": "circle",
                "color": "red",
                "size": 10
            },
            'support_para': {
                'type': 'pivot',
                'para': {
                    'type': 'low',
                    'filter': {
                        'min': 0,
                        'max': 35,
                    },
                    'bar_left': 3,
                    'bar_right': 3,

                }

            }
        },
        "rsi_resistance": {
            'target_ta': 'RSI',
            "type": "resistance",
            "y": "close",
            "subplot": 1,
            "marker": {
                "symbol": "circle",
                "color": "blue",
                "size": 10
            },
            'resistance_para': {
                'type': 'pivot',
                'para': {
                    'type': 'low',
                    'filter': {
                        'min': 75,
                        'max': 100,
                    },
                    'bar_left': 3,
                    'bar_right': 3,

                }

            }
        },
        "bull_zone": {
            "type": "zone",
            'target_ta': ["MA1", "MA2", "MA3"],
            'condition': "(MA1>=MA2) & (MA2>=MA3)",
            "subplot": 1,
            "fillcolor": 'green',

        }

    }
    visual = ChartVisualizer(ohlc_df, ta_paras, widget_paras)
    visual.get_app().run_server(host='127.0.0.1', debug=True, port=8005)
