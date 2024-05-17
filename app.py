import dash_bootstrap_components as dbc
from dash import Dash

from callbacks.callbacks import get_callbacks
from index import layout

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Cadre action anticipatoire ouragans Haïti : déclencheurs historiques"
app._favicon = "assets/favicon.ico"
server = app.server

app.layout = layout
get_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True)
