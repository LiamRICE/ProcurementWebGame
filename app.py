import dash
from dash import html, callback, dcc
from src.pages.main_page import main_page

# Create the app
app = dash.Dash(__name__)

# Define a layout for the app
app.layout = html.Div([
    main_page(),
    dcc.Location(id='url', refresh=False),
    dcc.Store(id='authentication', storage_type='memory', data={})
])

# Run the app
if __name__ == '__main__':
    app.run(debug=True)