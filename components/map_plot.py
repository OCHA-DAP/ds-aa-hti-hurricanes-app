import json

import pandas as pd
import plotly.graph_objects as go
from dash import dcc

from src.datasources import codab, nhc


def speed2cat(speed):
    if pd.isnull(speed):
        return None
    elif speed <= 33:
        return "TD"
    elif speed <= 63:
        return "TS"
    elif speed <= 82:
        return "1"
    elif speed <= 95:
        return "2"
    elif speed <= 112:
        return "3"
    elif speed <= 136:
        return "4"
    else:
        return "5"


monitors = nhc.load_hist_fcast_monitors()
tracks = nhc.load_hti_distances()
tracks["cat"] = tracks["windspeed"].apply(speed2cat)
tracks["lt"] = tracks["valid_time"] - tracks["issue_time"]
tracks = tracks.merge(
    monitors[monitors["lt_name"] == "readiness"], on=["atcf_id", "issue_time"]
)

lts = {
    "readiness": pd.Timedelta(days=5),
    "action": pd.Timedelta(days=3),
    "obsv": pd.Timedelta(days=0),
}

adm = codab.load_codab_from_blob(admin_level=0)
buffer = codab.load_buffer(distance_km=230)


def map_plot_fig(atcf_id: str, issue_time):
    tracks_f = tracks[
        (tracks["atcf_id"] == atcf_id)
        & (tracks["issue_time"].astype(str) == issue_time)
    ]
    issue_time_str = pd.to_datetime(issue_time).strftime("%Hh, %d %b")
    fig = go.Figure()
    for geom in adm.geometry[0].geoms:
        x, y = geom.exterior.coords.xy
        fig.add_trace(
            go.Scattermapbox(
                lon=list(x),
                lat=list(y),
                mode="lines",
                line_color="red",
                showlegend=False,
            )
        )
    fig.add_trace(
        go.Choroplethmapbox(
            geojson=json.loads(buffer.geometry.to_json()),
            locations=buffer.index,
            z=[1],
            colorscale="Reds",
            marker_opacity=0.2,
            showscale=False,
            marker_line_width=0,
            hoverinfo="none",
        )
    )

    dff_a = tracks_f[tracks_f["lt"] <= lts["action"]]
    dff_r = tracks_f[
        (tracks_f["lt"] <= lts["readiness"]) & (tracks_f["lt"] >= lts["action"])
    ]
    fig.add_trace(
        go.Scattermapbox(
            lon=dff_a["lon"],
            lat=dff_a["lat"],
            mode="text+lines",
            text=dff_a["windspeed"].astype(str),
            name="Prévision normale",
            line=dict(width=2, color="black"),
            textfont=dict(size=20, color="black"),
        )
    )
    fig.add_trace(
        go.Scattermapbox(
            lon=dff_r["lon"],
            lat=dff_r["lat"],
            mode="text+lines",
            text=dff_a["windspeed"].astype(str),
            name="Prévision prolongée",
            legendgroup=issue_time_str,
            line=dict(width=2, color="grey"),
            textfont=dict(size=20, color="grey"),
        )
    )
    fig.add_trace(
        go.Scattermapbox(
            lon=[-72.3],
            lat=[19],
            mode="text",
            text=[f'{dff_r["roll2_rain_dist"].max():.0f}'],
            name=issue_time_str,
            legendgroup=issue_time_str,
            textfont=dict(size=20, color="blue"),
        )
    )

    fig.update_layout(
        mapbox_style="open-street-map",
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        mapbox_zoom=5.8,
        mapbox_center_lat=19,
        mapbox_center_lon=-73,
        showlegend=False,
    )
    return fig


map_plot = dcc.Graph(
    id="map-plot",
    style={"height": "100vh", "background-color": "#f8f9fc"},
    config={"displayModeBar": False},
)
