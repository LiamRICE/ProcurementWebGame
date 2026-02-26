# Create a function that returns a Dash page for creating an account
from dash import html, dcc, callback, ctx, no_update
from dash.dependencies import Input, Output, State
from src.utils.user_utils import store_credentials

def create_account_page():
    layout = html.Div([
        # Title of the page
        html.H1('Create Account', style={'textAlign': 'center', 'color': '#00698f'}),
        
        # Form container with a header and footer
        html.Div([
            # Header with title and description
            html.Div([
                html.H2('Enter your credentials'),
                html.P('Please enter your username, email and password to create an account.')
            ], style={'marginTop': 20, 'marginBottom': 10}),

            html.Form([
                dcc.Input(id='username', type='text', placeholder='Username', style={'width': '100%'}),
                dcc.Input(id='password', type='password', placeholder='Password', style={'width': '100%', 'marginTop': 10}),

                html.Button('Submit', id='create-account-button', n_clicks=0, style={'background-color': '#00698f', 'color': '#ffffff', 'border': 'none', 'padding': '10px 20px', 'marginBottom': 20})
            ]),

            # Footer with output message
            html.Button('Have an account? Login', id="go-login-button", n_clicks=0, style={'marginTop': 30, 'fontSize': 16}),
        ], style={'width': '50%', 'margin': 'auto'}),
    ])
    
    return layout

@callback(
    Output('authentication', 'data', allow_duplicate=True),
    Output('url', 'pathname', allow_duplicate=True),
    Input('create-account-button', 'n_clicks'),
    State('username', 'value'),
    State('password', 'value'),
    prevent_initial_call=True
)
def create(n_clicks, username, password):
    print("Creating account : ", ctx.triggered_id, "with", n_clicks, "clicks.")
    # Check if all fields are filled out and click count is greater than 0
    if n_clicks > 0 and username != '' and password != '':
        print("Account created successfully")
        store_credentials(username, password)
        print("Returning authentication data and redirecting to homepage...")
        return {'authenticated': True, "user": username}, '/'
    else:
        return {}, '/create-account'



@callback(
    Output('url', 'pathname', allow_duplicate=True),
    Input('go-login-button', 'n_clicks'),
    prevent_initial_call=True
)
def go_to_login(n_clicks):
    print("Go to login page")
    if ctx.triggered_id == 'go-login-button' and n_clicks > 0:
        return '/login'
    return no_update