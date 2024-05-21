import dash_bootstrap_components as dbc
from dash import html

internal_alert = dbc.Alert(
    [
        "Ceci est un outil interne en cours de développement. "
        "Pour toute question, veuillez contacter le Centre de données "
        "humanitaires d'OCHA via Tristan Downing à l'addresse ",
        html.A("tristan.downing@un.org", href="mailto:tristan.downing@un.org"),
        ".",
    ],
    color="danger",
    dismissable=True,
)
