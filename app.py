import dash_bootstrap_components as dbc
from dash import Dash, html

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Tropical Cyclones Return Period"
app._favicon = "assets/favicon.ico"
server = app.server

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(
            html.A(
                html.Img(src="assets/centre_banner_greenbg.png", height=40),
                href="https://centre.humdata.org/anticipatory-action/",
            ),
            className="ml-2",
        ),
    ],
    style={"height": "60px", "margin": "0px"},
    brand="Tropical Cyclones Return Period Analysis",
    fixed="top",
    color="primary",
    dark=True,
)

app.layout = html.Div([navbar])


if __name__ == "__main__":
    app.run(debug=True)
