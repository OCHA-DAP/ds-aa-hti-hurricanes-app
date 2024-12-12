import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
from dash import dcc, html
from plotly.subplots import make_subplots


def time_plot_fig(atcf_id, app):
    monitors = app.data["monitors"]
    lts = app.data["lts"]
    triggers = app.data["triggers"]
    d_lim = 600

    df_storm = monitors.set_index("atcf_id").loc[atcf_id].reset_index()
    df_storm = df_storm[df_storm["dist_min"] < d_lim]

    df_storm["issue_time_str"] = df_storm["issue_time"].dt.strftime("%Hh, %d %b")
    name = df_storm.iloc[0]["name"]

    try:
        closest_time = triggers.set_index("atcf_id").loc[atcf_id]["closest_time"]
    except KeyError:
        closest_time = None
    min_time = df_storm["issue_time"].min()
    s_max = df_storm["wind_dist"].max()
    r_max = df_storm["roll2_rain_dist"].max()

    fig = make_subplots(rows=3, cols=1, shared_xaxes=True)
    shapes = []
    annotations = []
    prev_trig_time = pd.NaT
    for lt_name, params in lts.items():
        try:
            trig_time, trig_lt = triggers.set_index("atcf_id").loc[atcf_id][
                [lt_name, f"{lt_name}_lt"]
            ]
        except KeyError:
            trig_time = pd.NaT
            trig_lt = pd.NaT
        if prev_trig_time - trig_time < pd.Timedelta(days=1):
            offset = -0.2
            standoff = 80
        else:
            offset = -0.1
            standoff = 50
        if not pd.isnull(trig_time):
            shapes.append(
                {
                    "type": "line",
                    "xref": "x3",
                    "yref": "paper",
                    "x0": trig_time,
                    "x1": trig_time,
                    "y0": offset,
                    "y1": 1,
                    "line": {
                        "color": params.get("color"),
                        "width": 1,
                        "dash": "solid",
                    },
                }
            )
            annotations.append(
                {
                    "x": trig_time,
                    "y": offset,
                    "xref": "x3",
                    "yref": "paper",
                    "text": (
                        f'{params.get("label")} :<br>'
                        f'{trig_time.strftime("%-d %b, %-H:%M")}<br>'
                        f"(préavis {trig_lt.total_seconds() / 3600:.0f} heures)"
                    ),
                    "showarrow": False,
                    "xanchor": "center",
                    "yanchor": "top",
                    "font": {"size": 10, "color": params.get("color")},
                }
            )

        df_plot = df_storm[df_storm["lt_name"] == lt_name]
        for j, var in enumerate(["wind_dist", "roll2_rain_dist", "dist_min"]):
            mode = "markers" if len(df_plot[var].dropna()) == 1 else "lines"
            fig.add_trace(
                go.Scatter(
                    x=df_plot["issue_time"],
                    y=df_plot[var],
                    mode=mode,
                    name=params["label"],
                    line_color=params.get("color"),
                    line_dash=params.get("dash"),
                    line_width=3,
                ),
                row=j + 1,
                col=1,
            )
            shapes.append(
                {
                    "type": "line",
                    "xref": "paper",
                    "yref": f"y{j+1}",
                    "x0": 0,
                    "x1": 1,
                    "y0": params["threshs"][var],
                    "y1": params["threshs"][var],
                    "line": {
                        "color": params["color"],
                        "width": 1,
                        "dash": "dash",
                    },
                }
            )
        prev_trig_time = trig_time

    # zero lines
    shapes.extend(
        [
            {
                "type": "line",
                "xref": "paper",
                "yref": f"y{x}",
                "x0": 0,
                "x1": 1,
                "y0": 0,
                "y1": 0,
                "line": {"color": "black", "width": 2},
            }
            for x in [1, 2]
        ]
    )

    # closest pass
    if closest_time is not None:
        shapes.append(
            {
                "type": "line",
                "xref": "x3",
                "yref": "paper",
                "x0": closest_time,
                "x1": closest_time,
                "y0": -0.1,
                "y1": 1,
                "line": {"color": "black", "width": 2, "dash": "solid"},
            }
        )
        annotations.append(
            {
                "x": closest_time,
                "y": -0.1,
                "xref": "x3",
                "yref": "paper",
                "text": f'Passage plus proche :<br>{closest_time.strftime("%-d %b, %H:%M")}',
                "showarrow": False,
                "xanchor": "center",
                "yanchor": "top",
                "font": {"size": 10, "color": "black"},
            }
        )

    yaxis_font_size = 14
    fig.update_traces(xaxis="x3")
    fig.update_layout(
        hovermode="x unified",
        title=f"Prévisions de ouragan {name}<br><sup>"
        "Graphiques indiquent valeurs prévues; "
        "lignes en tirets indiquent seuils</sup>",
        yaxis=dict(
            title=dict(
                text="Vitesse<br>de vent<br>(noeuds)",
                font_size=yaxis_font_size,
            ),
            range=[0, s_max + 10],
        ),
        yaxis2=dict(
            title=dict(
                text="Précipitations<br>sur 2 jours<br>(mm)",
                font_size=yaxis_font_size,
            ),
            range=[0, r_max + 10],
        ),
        yaxis3=dict(
            title=dict(text="Distance<br>minimum<br>(km)", font_size=yaxis_font_size),
            range=[0, d_lim],
        ),
        xaxis3=dict(
            title=dict(text="Heure de publication de prévision", standoff=standoff),
            range=[min_time, closest_time + pd.Timedelta(days=0.5)],
        ),
        shapes=shapes,
        annotations=annotations,
        template="simple_white",
        height=630,
        width=600,
        showlegend=False,
        margin={"b": 100, "t": 40, "l": 50, "r": 20},
    )
    return fig


time_plot = dcc.Graph(id="time-plot", config={"displayModeBar": False})

time_plot_collapse = html.Div(
    [
        dbc.Button(
            "Afficher/masquer chronologie",
            id="collapse-button",
            className="align-self-end mb-2",
            color="light",
            n_clicks=0,
        ),
        dbc.Collapse(
            dbc.Card(html.Div(time_plot, className="m-1")),
            id="collapse",
            className="ml-auto",
            is_open=False,
        ),
    ],
    className="d-flex flex-column justify-content-end",
)
