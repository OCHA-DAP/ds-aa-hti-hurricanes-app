import dash_bootstrap_components as dbc
from dash import html

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(
            html.A(
                html.Img(src="assets/centre_banner_greenbg.png", height=40),
                href="https://centre.humdata.org/anticipatory-action/",
            ),
        ),
    ],
    style={"height": "60px", "margin": "0px", "padding": "10px"},
    brand="Cadre action anticipatoire ouragans Haïti : déclencheurs historiques",
    fixed="top",
    color="primary",
    dark=True,
    fluid=True,
)
