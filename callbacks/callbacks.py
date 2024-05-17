from dash.dependencies import Input, Output

from components.map_plot import map_plot_fig


def get_callbacks(app):
    @app.callback(
        Output("map-plot", "figure"),
        Input("storm-dropdown", "value"),
    )
    def update_map_plot_fig(atcf_id):
        return map_plot_fig(atcf_id)
