import locale

import dash_bootstrap_components as dbc
from dash import Dash

from callbacks.callbacks import register_callbacks
from data.load_data import load_data
from index import layout

locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Cadre action anticipatoire ouragans Haïti : déclencheurs historiques"
app._favicon = "assets/favicon.ico"
server = app.server

app.data = load_data()

app.layout = layout(app)
register_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True)
