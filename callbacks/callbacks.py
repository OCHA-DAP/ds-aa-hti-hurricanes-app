from dash.dependencies import Input, Output, State

from components.map_plot import map_plot_fig


def register_callbacks(app):
    @app.callback(
        Output("map-plot", "figure"),
        Input("date-dropdown", "value"),
        State("storm-dropdown", "value"),
    )
    def update_map_plot_fig(issue_time, atcf_id):
        return map_plot_fig(atcf_id, issue_time, app)

    @app.callback(
        Output("date-dropdown", "options"),
        Output("date-dropdown", "value"),
        Input("storm-dropdown", "value"),
    )
    def update_date_dropdown_options(atcf_id):
        monitors = app.data["monitors"]
        issue_times = monitors[monitors["atcf_id"] == atcf_id]["issue_time"].unique()
        return [
            {"label": i.strftime("%Hh, %d %b"), "value": str(i)} for i in issue_times
        ], str(issue_times[0])
