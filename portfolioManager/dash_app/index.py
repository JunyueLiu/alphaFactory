import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from portfolioManager.dash_app.app import app


def get_pm_report_dash_app(portfolios:dict):
    # portfolio
    # {
    #   'strategy_1':{
    #   'net_value': pd.Series,
    #   'position': pd.DataFrame
    #
    #
    #
    #   }
    # 'strategy_2':
    # {
    #   'net_value': pd.Series,
    #   'position': pd.DataFrame
    #
    #
    #
    #   }
    #
    #
    #
    # }


    app.layout = html.Div([])




if __name__ == '__main__':
    app_ = get_pm_report_dash_app()
    # app.run_server(host='127.0.0.1')