from dash import html, dcc, callback, Output, Input, State, no_update, ctx


def navbar(
    home_href="/",
    mode="login",
    disconnect_id="disconnect-button",
    navbar_id="navbar",
):
    dropdowns = dropdowns_by_mode(mode)

    nav_dropdowns = []
    for menu in dropdowns:
        nav_dropdowns.append(
            html.Div(
                [
                    html.Button(
                        menu["label"],
                        className="nav-dropbtn",
                    ),
                    html.Div(
                        [
                            dcc.Link(
                                item["label"],
                                href=item.get("href", "#"),
                                className="nav-dropdown-link",
                            )
                            for item in menu["items"]
                        ],
                        className="nav-dropdown-content",
                    ),
                ],
                className="nav-dropdown",
            )
        )

    navbar = html.Div(
        [
            html.Div(
                [
                    dcc.Link("🏠 Home", href=home_href, className="nav-home"),
                    *nav_dropdowns,
                ],
                className="nav-left",
            ),
            html.Button(
                "Disconnect",
                id=disconnect_id,
                n_clicks=0,
                className="nav-disconnect",
            ),
        ],
        id=navbar_id,
        className="nav-bar",
    )

    return navbar



def dropdowns_by_mode(mode="login"):
    if mode == "login":
        dropdowns = []
    else:
        dropdowns=[
            {
                "label": "Nation",
                "id": "nation-menu",
                "items": [
                    {"label": "Regions", "href": "/regions"},
                    {"label": "National Budget", "href": "/budget"},
                    {"label": "National Policies", "href": "/policies"},
                    {"label": "International Relations", "href": "/international-relations"},
                ],
            },
            {
                "label": "Objectives",
                "id": "objectives-menu",
                "items": [
                    {"label": "Capabilities", "href": "/capabilities"},
                    {"label": "Rival Nations", "href": "/rival-nations"},
                ],
            },
            {
                "label": "Finances",
                "id": "objectives-menu",
                "items": [
                    {"label": "Military Budget", "href": "/military-budget"},
                    {"label": "Military Expenses", "href": "/military-expenses"},
                ],
            },
        ]
    
    return dropdowns



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
