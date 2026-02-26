from dash import html, dcc, callback, Output, Input, State, no_update, ctx


def navbar(
    home_href="/",
    dropdowns=None,
    disconnect_id="disconnect-button",
    navbar_id="navbar",
):
    """
    Creates a reusable Dash navbar.

    Parameters
    ----------
    home_href : str
        URL for the home button.
    dropdowns : list of dict
        Example:
        [
            {
                "label": "File",
                "items": [
                    {"label": "Open", "value": "open"},
                    {"label": "Save", "value": "save"},
                ],
                "id": "file-menu"
            }
        ]
    disconnect_id : str
        Component ID for disconnect button.
    navbar_id : str
        Navbar container ID.

    Returns
    -------
    html.Div
    """

    dropdowns = dropdowns or []

    dropdown_components = []
    for menu in dropdowns:
        dropdown_components.append(
            html.Div(
                [
                    html.Label(menu["label"], className="navbar-label"),
                    dcc.Dropdown(
                        id=menu["id"],
                        options=[
                            {"label": item["label"], "value": item["value"]}
                            for item in menu["items"]
                        ],
                        placeholder=menu["label"],
                        clearable=False,
                        className="navbar-dropdown",
                    ),
                ],
                className="navbar-item",
            )
        )

    navbar = html.Div(
        [
            # Left side
            html.Div(
                [
                    dcc.Link(
                        html.Button("🏠 Home", className="navbar-button"),
                        href=home_href,
                    ),
                    *dropdown_components,
                ],
                className="navbar-left",
            ),

            # Right side
            html.Div(
                html.Button(
                    "Disconnect",
                    id=disconnect_id,
                    n_clicks=0,
                    className="disconnect-button",
                ),
                className="navbar-right",
            ),
        ],
        id=navbar_id,
        className="navbar",
        style={
            "display": "flex",
            "justifyContent": "space-between",
            "alignItems": "center",
            "padding": "10px",
            "backgroundColor": "#2c3e50",
        },
    )

    return navbar


@callback(
    Output("authentication", "data", allow_duplicate=True),
    Output("url", "pathname", allow_duplicate=True),
    Input("disconnect-button", "n_clicks"),
    State("authentication", "data"),
    prevent_initial_call=True
)
def disconnect_user(n_clicks, auth_data):
    print("Disconnect triggered : ", ctx.triggered_id, "with", n_clicks, "clicks.")
    if ctx.triggered_id == "disconnect-button" and n_clicks > 0:
        print("Disconnecting...")
        # Ensure dict exists
        auth_data = auth_data or {}

        # Update authentication state
        auth_data["authenticated"] = False
        auth_data["user"] = None

        return auth_data, "/login"

    else:
        return no_update, no_update
