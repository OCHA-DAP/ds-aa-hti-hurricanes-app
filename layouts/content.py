import dash_bootstrap_components as dbc
from dash import dcc, html

from components.alerts import internal_alert
from components.date_dropdown import date_dropdown
from components.map_plot import map_plot
from components.storm_dropdown import get_storm_dropdown
from components.time_plot import time_plot_collapse


def content(app):
    return html.Div(
        [
            html.Div(
                style={
                    "position": "fixed",
                    "top": 60,
                    "left": 0,
                    "bottom": 0,
                    "zIndex": 1,
                },
                children=[
                    # top left
                    html.Div(
                        style={"position": "absolute", "top": 0, "left": 0},
                        children=[
                            html.Div(internal_alert, className="m-2"),
                            html.Div(get_storm_dropdown(app), className="m-2"),
                            html.Div(date_dropdown, className="m-2"),
                        ],
                    ),
                    # bottom left
                    html.Div(
                        style={"position": "absolute", "bottom": 0, "left": 0},
                        children=[
                            dbc.Card(
                                html.Img(
                                    src="assets/map_legend.png",
                                    height=300,
                                    className="m-1",
                                ),
                                className="m-2",
                            )
                        ],
                    ),
                ],
            ),
            # top right
            html.Div(
                style={
                    "position": "fixed",
                    "top": 60,
                    "right": 0,
                    "zIndex": 1,
                },
                children=[
                    html.Div(time_plot_collapse, className="m-2"),
                ],
            ),
            html.Div(
                style={
                    "position": "fixed",
                    "top": 60,
                    "left": 0,
                    "bottom": 0,
                    "right": 0,
                    "zIndex": 0,
                },
                children=dcc.Loading(
                    map_plot,
                    parent_className="loading_wrapper",
                ),
            ),
        ]
    )
