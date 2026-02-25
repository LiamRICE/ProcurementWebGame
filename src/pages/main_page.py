import dash
from dash import html, callback
from dash.dependencies import Input, Output, State
from src.pages.authentication.login import login_page
from src.pages.authentication.create_account import create_account_page

def main_page():

    # Create a simple layout with a title and a paragraph of text.
    return html.Div([
        html.Div(id='content-div', children=[])
    ])


# Define the callback to manage URL navigation
@callback(
    Output('content-div', 'children'),
    State('authentication', 'data'),
    Input('url', 'pathname')
)
def update_url(auth_data, url):
    print(auth_data, url)
    if auth_data is None:
        auth_data = {}

    if auth_data.get('authenticated', False) == False and url not in ['/login', '/create-account']:
        url = '/login'  # Redirect to login page if not authenticated*
    elif auth_data.get('authenticated', False) == True and url in ['/login', '/create-account']:
        url = '/'  # Redirect to homepage if already authenticated
    # If the user navigates away from the root URL ('/'), redirect back to it
    if url == '/':
        return html.P("This is the homepage")
    elif url == '/login':
        return login_page()
    elif url == '/create-account':
        return create_account_page()
    else:
        return html.P("Error 404: Page not found")



