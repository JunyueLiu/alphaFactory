import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from backtesting.dash_app import entry_exit_analysis
from backtesting.dash_app import monthly_analysis
from backtesting.dash_app import trading_history
from backtesting.dash_app import dash_report


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H2('Backtesting Result'),
    dcc.Location(id='url', refresh=False),
    dcc.Link('General Performance', href='/btPerformance'),
    html.Br(),
    dcc.Link('Monthly Analysis', href='/monthlyAnalysis'),
    html.Br(),
    dcc.Link('Entry and exit Detail', href='/details'),
    html.Br(),
    dcc.Link('Trading history', href='/history'),
    html.Div(id='page-content')
])



index_page = html.Div([
    # todo 行情profile
    # benchmark
    # each stock
    # each time frame

    # todo 回测类型
    #
]),


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/btPerformance':
        return dash_report.layout
    elif pathname == '/monthlyAnalysis':
        return monthly_analysis.layout
    elif pathname == '/details':
        return entry_exit_analysis.layout
    elif pathname == 'history':
        return trading_history.layout

    else:
        return index_page



if __name__ == '__main__':
    app.run_server(host='127.0.0.1', debug=True)