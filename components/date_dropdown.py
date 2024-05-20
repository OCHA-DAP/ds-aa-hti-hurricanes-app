import dash_bootstrap_components as dbc

date_dropdown = dbc.InputGroup(
    [
        dbc.InputGroupText("Heure de publication"),
        dbc.Select(
            id="date-dropdown",
        ),
    ],
    style={
        "width": "350px",
    },
)
