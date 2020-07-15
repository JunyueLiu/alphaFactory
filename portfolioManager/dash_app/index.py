from datetime import timedelta

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from portfolioManager.dash_app.app import app
from portfolioManager.plotting import net_values_plot, corr_heatmap, holding_line_plot
from portfolioManager.utils import *


def get_pm_report_dash_app(portfolio: dict = None):
    # portfolio
    # {
    #   'strategy_1':{
    #   'net_value': pd.Series,
    #   'position': pd.Series
    #
    #
    #
    #   }
    # }
    net_values = to_net_value_df(portfolio)
    pos = to_position_df(portfolio)
    instruments = pos.index.get_level_values(1).unique().to_list()

    min_date = net_values.index.get_level_values(0).min().date()
    max_date = net_values.index.get_level_values(0).max().date()

    net_values_ts_plot = net_values_plot(net_values)
    rets = net_values.pct_change()
    corr_heatmap_plot = corr_heatmap(rets.corr())

    app.layout = html.Div([
        html.H1('Strategy Comparison'),
        dcc.Graph(figure=net_values_ts_plot),
        dcc.Graph(figure=corr_heatmap_plot),
        dcc.Dropdown(id='asset-selection',
                     options=[
                         {'label': i, 'value': i} for i in instruments

                     ], value=instruments[0]),
        dcc.DatePickerRange(id='date-range',
                            min_date_allowed=min_date,
                            max_date_allowed=max_date,
                            initial_visible_month=max_date,
                            start_date=max_date - timedelta(days=20),
                            end_date=max_date
                            ),
        dcc.Graph(id='holding'),



    ])


    @app.callback([Output('holding', 'figure')],
                  [Input('asset-selection', 'value'),
                   Input('date-range', 'start_date'),
                   Input('date-range', 'end_date'),])
    def update_holding(instrument, start_date, end_date):
        return holding_line_plot(pos, instrument, start_date, end_date),


if __name__ == '__main__':
    portfolio = load_result_from_pickles(r'../sample_data')
    portfolio = normalized_net_value(portfolio)
    # print(portfolio)
    app_ = get_pm_report_dash_app(portfolio)
    app.run_server(host='127.0.0.1', debug=True)
