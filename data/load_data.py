import pandas as pd

from src.datasources import codab, nhc
from src.utils.processing import speed2cat


def load_data():
    monitors = nhc.load_hist_fcast_monitors()
    tracks = nhc.load_hti_distances()
    tracks["cat"] = tracks["windspeed"].apply(speed2cat)
    tracks["lt"] = tracks["valid_time"] - tracks["issue_time"]
    tracks = tracks.merge(
        monitors[monitors["lt_name"] == "readiness"], on=["atcf_id", "issue_time"]
    )
    storms = monitors.groupby("atcf_id")["name"].first().reset_index()
    storms["year"] = storms["atcf_id"].str[-4:].astype(int)
    storms = storms.sort_values(["year", "name"], ascending=False)
    storms["nameyear"] = storms["name"] + " " + storms["year"].astype(str)
    storms = storms.set_index("atcf_id")

    adm = codab.load_codab_from_blob(admin_level=0)
    buffer = codab.load_buffer(distance_km=230)

    lts = {
        "readiness": pd.Timedelta(days=5),
        "action": pd.Timedelta(days=3),
        "obsv": pd.Timedelta(days=0),
    }

    return {
        "monitors": monitors,
        "tracks": tracks,
        "storms": storms,
        "adm": adm,
        "buffer": buffer,
        "lts": lts,
    }
