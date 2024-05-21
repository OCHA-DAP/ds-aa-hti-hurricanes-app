import json

import pandas as pd
import plotly.graph_objects as go
from dash import dcc


def map_plot_fig(atcf_id: str, issue_time, app):
    adm = app.data["adm"]
    buffer = app.data["buffer"]
    tracks = app.data["tracks"]
    lts = app.data["lts"]
    tracks_f = tracks[
        (tracks["atcf_id"] == atcf_id)
        & (tracks["issue_time"].astype(str) == issue_time)
    ]
    issue_time_str = pd.to_datetime(issue_time).strftime("%Hh, %d %b")
    fig = go.Figure()
    # adm0 outline
    for geom in adm.geometry[0].geoms:
        x, y = geom.exterior.coords.xy
        fig.add_trace(
            go.Scattermapbox(
                lon=list(x),
                lat=list(y),
                mode="lines",
                line_color="grey",
                showlegend=False,
            )
        )
    # buffer
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

    for lt_name in ["readiness", "action"]:
        lt_params = lts[lt_name]
        dff = tracks_f[
            (tracks_f["lt"] <= lt_params["lt_max"])
            & (tracks_f["lt"] >= lt_params["lt_min"])
        ]
        # triggered points
        dff_trig = dff[dff["windspeed"] >= lt_params["threshs"]["wind_dist"]]
        fig.add_trace(
            go.Scattermapbox(
                lon=dff_trig["lon"],
                lat=dff_trig["lat"],
                mode="markers",
                marker=dict(size=50, color="red"),
            )
        )
        # all points
        fig.add_trace(
            go.Scattermapbox(
                lon=dff["lon"],
                lat=dff["lat"],
                mode="markers+text+lines",
                marker=dict(size=40, color=lt_params["plot_color"]),
                text=dff["windspeed"].astype(str),
                name="Prévision normale",
                line=dict(width=2, color=lt_params["plot_color"]),
                textfont=dict(size=20, color="white"),
            )
        )

        # rainfall
        if lt_name == "readiness":
            rain_level = dff["roll2_rain_dist"].max()
            if pd.isnull(rain_level):
                rain_level_str = ""
            else:
                rain_level_str = int(rain_level)
            if rain_level > lt_params["threshs"]["roll2_rain_dist"]:
                fig.add_trace(
                    go.Scattermapbox(
                        lon=[-72.3],
                        lat=[19],
                        mode="markers",
                        marker=dict(size=50, color="red"),
                    )
                )
            fig.add_trace(
                go.Scattermapbox(
                    lon=[-72.3],
                    lat=[19],
                    mode="text+markers",
                    text=[rain_level_str],
                    marker=dict(size=40, color="blue"),
                    name=issue_time_str,
                    textfont=dict(size=20, color="white"),
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
    style={"height": "100vh"},
    config={"displayModeBar": False},
)
