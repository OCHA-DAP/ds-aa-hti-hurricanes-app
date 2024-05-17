import dash_bootstrap_components as dbc

date_dropdown = dbc.Select(
    id="date-dropdown",
    style={
        "position": "fixed",
        "width": "200px",
        "top": 100,
        "left": 20,
        "zIndex": 1,
    },
)
