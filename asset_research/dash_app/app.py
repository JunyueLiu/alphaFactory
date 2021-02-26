import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)


# app.validation_layout = html.Div([
#             ,
#             general_div,
#             quantile_div,
#             group_div
#
#         ])


def get_asset_study_dash_app(dash_app=None):
    # global app
    if dash_app is not None:
        app_ = dash_app
    else:
        app_ = app
    app_.layout = html.Div([
        html.H2('Asset Study'),
        dcc.Location(id='url', refresh=False),
        dcc.Link('Index', href='/'),
        html.Br(),
        dcc.Link('technical analysis', href='/technicalStudy'),
        html.Br(),
        dcc.Link('return study', href='/returnStudy'),
        html.Br(),
        dcc.Link('labelling study', href='/LabellingStudy'),
        html.Br(),
        dcc.Link('intraday study', href='/intradayStudy'),
        html.Br(),
        dcc.Link('filter study', href='/filter'),
        html.Br(),

        html.Div(id='page-content'),
    ], style={'margin': '30px'})

    # --------------- index page callback ---------------
    @app.callback(Output('page-content', 'children'),
                  [Input('url', 'pathname')])
    def display_page(pathname):
        if pathname == '/technicalStudy':
            return dash_app.get_layout()
        elif pathname == '/monthlyAnalysis':
            return monthly_analysis.get_layout(backtesting_result)
        elif pathname == '/details':
            return entry_exit_analysis.get_layout(backtesting_result)
        elif pathname == '/history':
            return trading_history.get_layout(backtesting_result)
        elif pathname == '/filter':
            return filter_out_study.get_layout(backtesting_result)
        else:
            return

    return app_
