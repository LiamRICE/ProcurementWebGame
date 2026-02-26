import dash
from dash import dcc, html, callback, Output, Input
import dash_bootstrap_components as dbc


def main_page():
    login_state = dcc.Store(id="authentication", data=None)
    url_state = dcc.Location(id="url", refresh=False)

    return html.Div(
        children=[
            # header
            html.H1("Army Procurement Game"),
            html.P("Game about army procurement"),
            login_state,
            url_state,
            html.Div(id="page-body", children=[])
        ]
    )



@callback(
    Output("page-content", "children"),
    Output("top-component", "children"),
    Input("url", "pathname"),
    Input("authentication", "data")
)
def display_page(pathname, authentication):
    username = authentication.get("username", "guest")

    if authentication == None:
        pathname = "/login"
    
    if pathname == "/":
        pass
    else:
        return "Error 404 - Page does not exist"