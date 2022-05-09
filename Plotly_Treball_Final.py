import dash
import dash_bootstrap_components as dbc
from dash import html
import dash_core_components as dcc
import plotly.graph_objects as go
import pandas as pd
import base64

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions = True

def encode_image(image_file):
    encoded = base64.b64encode(open(image_file, 'rb').read())
    return 'data:image/png;base64,{}'.format(encoded.decode())

navbar = dbc.Navbar(
    [dbc.NavbarBrand("Cloud Recognition", style={'textAlign': 'center', 'color': 'white', 'fontSize':'30px'}),
        html.Div(id='dd-output-container')
    ],
    color='black',
    style={'color': 'black',  'textAlign': 'center', 'justifyContent': 'center'}
)



app.layout = html.Div(children=[navbar,
                                dbc.Row([
                                    dbc.Col(
                                        html.Div([dcc.Upload(
                                                        id="upload-data",
                                                        children=html.Div(["Arrossega la imatge que vulguis o selecciona l'arxiu"]),
                                                        # Allow multiple files to be uploaded
                                                        multiple=False,
                                                        )]), width=12)]),
                                    html.Div(html.Footer(["Cloud Recognition Los del Fondo"], id='footer-text'), id='footer')])
if __name__ == '__main__':
    app.run_server(debug=True)