from dash import Dash, callback, html, dcc, no_update
from dash.dependencies import Input, Output, State
from src.utils.user_utils import check_credentials

def login_page():
# Define the layout for the page
    layout = html.Div([
        # Title of the page
        html.H1('Login Page', style={'textAlign': 'center', 'color': '#00698f'}),
        # Form container with a header and footer
        html.Div([
            # Header with title and description
            html.Div([
                html.H2('Enter your credentials'),
                html.P('Please enter your username and password to log in.')
            ], style={'marginTop': 20, 'marginBottom': 10}),
            html.Form([
                dcc.Input(id='username', type='text', placeholder='Username', style={'width': '100%'}),
                dcc.Input(id='password', type='password', placeholder='Password', style={'width': '100%', 'marginTop': 10}),
                html.Button('Submit', id='login-button', n_clicks=0, style={'background-color': '#00698f', 'color': '#ffffff', 'border': 'none', 'padding': '10px 20px', 'marginBottom': 20})
            ]),
            html.Div([
                html.A('Don\'t have an account?', href='/create-account', style={'marginRight': 10}),
                html.Button('Create Account', id='create-account-button', n_clicks=0, style={'background-color': '#00698f', 'color': '#ffffff', 'border': 'none', 'padding': '10px 20px'})
            ], style={'textAlign': 'center', 'marginBottom': 40}),

            # Footer with output message
            html.Div(id='output', style={'marginTop': 30, 'fontSize': 16})
        ], style={'width': '50%', 'margin': 'auto'})
    ])

    return layout

@callback(
    Output('authentication', 'data', allow_duplicate=True),
    Input('login-button', 'n_clicks'),
    State('username', 'value'),
    State('password', 'value'),
    prevent_initial_call=True
)
def login(n_clicks, username, password):
    if n_clicks > 0 and username != '' and password != '':
        print("Attempting login...")
        if check_credentials(username, password):
            return {'authenticated': True, 'user': username}
        else:
            return no_update
