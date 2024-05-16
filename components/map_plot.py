import json

import pandas as pd
import plotly.graph_objects as go
from dash import dcc

from src.constants import MATTHEW_ATCF_ID
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


def plot_forecast_map(atcf_id):
    tracks_f = tracks[tracks["atcf_id"] == atcf_id]
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
    visible = True
    for issue_time, group in tracks_f.groupby("issue_time"):
        issue_time_str = issue_time.strftime("%-d %b, %H:%M")
        dff_a = group[group["lt"] <= lts["action"]]
        dff_r = group[
            (group["lt"] <= lts["readiness"]) & (group["lt"] >= lts["action"])
        ]
        fig.add_trace(
            go.Scattermapbox(
                lon=dff_a["lon"],
                lat=dff_a["lat"],
                mode="text+lines",
                text=dff_a["windspeed"].astype(str),
                name=issue_time_str,
                legendgroup=issue_time_str,
                line=dict(width=2, color="black"),
                textfont=dict(size=20, color="black"),
                visible=visible,
                showlegend=True,
                # legendgrouptitle_text=issue_time_str,
            )
        )
        fig.add_trace(
            go.Scattermapbox(
                lon=dff_r["lon"],
                lat=dff_r["lat"],
                mode="text+lines",
                text=dff_a["windspeed"].astype(str),
                name=issue_time_str,
                legendgroup=issue_time_str,
                line=dict(width=2, color="grey"),
                textfont=dict(size=20, color="grey"),
                visible=visible,
                showlegend=False,
                legendgrouptitle_text="",
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
                visible=visible,
                showlegend=False,
                legendgrouptitle_text="",
            )
        )
        visible = "legendonly"

    fig.update_layout(
        mapbox_style="open-street-map",
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        mapbox_zoom=5.8,
        mapbox_center_lat=19,
        mapbox_center_lon=-73,
    )
    return fig


map_plot = dcc.Graph(
    figure=plot_forecast_map(MATTHEW_ATCF_ID),
    id="map-content",
    style={"height": "100vh", "background-color": "#f8f9fc"},
    config={"displayModeBar": False},
)
