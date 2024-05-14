from dash import dcc, html

from components.map_plot import map_plot

content = html.Div(
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
)
