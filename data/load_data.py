import pandas as pd

from src.datasources import codab, nhc
from src.utils import blob
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
        "action": {
            "color": "darkorange",
            "plot_color": "black",
            "dash": "solid",
            "label": "Action",
            "zorder": 2,
            "lt_max": pd.Timedelta(days=3),
            "lt_min": pd.Timedelta(days=0),
            "threshs": {
                "roll2_rain_dist": 42,
                "wind_dist": 64,
                "dist_min": 230,
            },
        },
        "readiness": {
            "color": "dodgerblue",
            "plot_color": "grey",
            "dash": "dot",
            "label": "Mobilisation",
            "zorder": 1,
            "lt_max": pd.Timedelta(days=5),
            "lt_min": pd.Timedelta(days=3),
            "threshs": {
                "roll2_rain_dist": 35,
                "wind_dist": 34,
                "dist_min": 230,
            },
        },
    }

    trig_str = (
        f'triggers_r_p{lts["readiness"]["threshs"]["roll2_rain_dist"]}_s{lts["readiness"]["threshs"]["wind_dist"]}_'
        f'a_p{lts["action"]["threshs"]["roll2_rain_dist"]}_s{lts["action"]["threshs"]["wind_dist"]}'
    )
    blob_name = f"{blob.PROJECT_PREFIX}/processed/{trig_str}.csv"
    triggers = blob.load_parquet_from_blob(blob_name, prod_dev="dev")

    return {
        "monitors": monitors,
        "tracks": tracks,
        "storms": storms,
        "adm": adm,
        "buffer": buffer,
        "lts": lts,
        "triggers": triggers,
    }
