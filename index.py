from dash import html

from layouts.content import content
from layouts.navbar import navbar

layout = html.Div([navbar, content])
