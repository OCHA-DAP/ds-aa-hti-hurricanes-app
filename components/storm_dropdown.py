import dash_bootstrap_components as dbc

from src.constants import MATTHEW_ATCF_ID
from src.datasources import nhc

monitors = nhc.load_hist_fcast_monitors()
storms = monitors.groupby("atcf_id")["name"].first().reset_index()
storms["year"] = storms["atcf_id"].str[-4:].astype(int)
storms = storms.sort_values(["year", "name"], ascending=False)
storms["nameyear"] = storms["name"] + " " + storms["year"].astype(str)
storms = storms.set_index("atcf_id")


storm_dropdown = dbc.Select(
    id="storm-dropdown",
    value=MATTHEW_ATCF_ID,
    options=[
        {"label": nameyear, "value": atcf_id, "className": "bold-option"}
        for atcf_id, nameyear in storms["nameyear"].items()
    ],
    style={
        "width": "200px",
    },
)
