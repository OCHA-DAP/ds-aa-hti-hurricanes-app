import dash_bootstrap_components as dbc

from src.constants import MATTHEW_ATCF_ID


def get_storm_dropdown(app):
    storms = app.data["storms"]
    return dbc.InputGroup(
        [
            dbc.InputGroupText("Tempête"),
            dbc.Select(
                id="storm-dropdown",
                value=MATTHEW_ATCF_ID,
                options=[
                    {"label": nameyear, "value": atcf_id, "className": "bold-option"}
                    for atcf_id, nameyear in storms["nameyear"].items()
                ],
            ),
        ],
        style={
            "width": "350px",
        },
    )
