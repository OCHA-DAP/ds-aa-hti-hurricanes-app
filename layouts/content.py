from dash import dcc, html

from components.date_dropdown import date_dropdown
from components.map_plot import map_plot
from components.storm_dropdown import get_storm_dropdown


def content(app):
    return html.Div(
        [
            html.Div(
                style={
                    "position": "fixed",
                    "top": 60,
                    "left": 0,
                    "width": "100%",
                    "zIndex": 1,
                },
                children=[
                    html.Div(get_storm_dropdown(app), className="m-2"),
                    html.Div(date_dropdown, className="m-2"),
                ],
            ),
            html.Div(
                style={
                    "position": "fixed",
                    "top": 60,
                    "left": 0,
                    "width": "100%",
                    "zIndex": 0,
                },
                children=dcc.Loading(
                    map_plot,
                    parent_className="loading_wrapper",
                ),
            ),
        ]
    )
