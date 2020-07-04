import dash
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)

# app.validation_layout = html.Div([
#             ,
#             general_div,
#             quantile_div,
#             group_div
#
#         ])
