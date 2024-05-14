from dash import dcc

content = dcc.Loading(
    dcc.Graph(
        # figure=init_fig,
        id="graph-content",
        style={"height": "100vh", "background-color": "#f8f9fc"},
        config={"displayModeBar": False},
    ),
    parent_className="loading_wrapper",
)
