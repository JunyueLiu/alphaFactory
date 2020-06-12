from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
# from web.hsi_intraday_app import app as hsi_app
app = Flask(__name__)
bootstrap = Bootstrap(app)
# dash_app = Dash(__name__,
#                server=app)
# dash_app.layout = html.Div(id='dash-container')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('coming.html')

@app.route('/contact')
def contact():
    return render_template('coming.html')

@app.route('/progress')
def progress():
    return render_template('progress.html')

@app.route('/example')
def example():
    return render_template('coming.html')


@app.route('/document')
def document():
    return render_template('coming.html')

@app.route('/comingsoon')
def comingsoon():
    return render_template('coming.html')

# @app.route('/hsiIntraday')
# def hsi_live():
#     return dash_app.index()


#
#
if __name__ == '__main__':
    app.run(debug=True)