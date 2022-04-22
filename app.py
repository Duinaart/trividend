import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc


from callbacks import register_callbacks_info

"""
- 
"""

# from market_overview import body4
# Light theme: LUX, dark theme: DARKLY (enable darktheme in navbar)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])
server = app.server
app.config['suppress_callback_exceptions'] = True

######################################################################################################################
#! Import function
######################################################################################################################
from functions import unique_firms
######################################################################################################################
#! Navbar and tabs
######################################################################################################################

# make dropdown for selecting firms
dropdown = dcc.Dropdown(
    options=unique_firms,
    value='de wassende maan',
    id='dropdown'
)

# make text input for selecting firms
# text_input = dbc.Input(id='input', type="search", placeholder="Search here",value='de wassende maan',
#                        debounce=True, className="flex-grow-1")

# make navigation bar
navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Div(html.Img(src='https://evpa.eu.com/uploads/images/Trividend.jpg', height="20px")), width=2 ),
                        dbc.Col(html.Div(dbc.NavbarBrand("Financial Dashboard Portfolio Trividend", className="ms-2",)), width=7),
                        dbc.Col(html.Div(dropdown), width=3),
                    ], justify='center',  className="ms-auto mt-md-0 flex-grow-1 flex-nowrap",
                ),  className="ms-auto mt-md-0 flex-grow-1 flex-nowrap", style={"textDecoration": "none"},
            ),
        ]
    ),
    color="white"
)

navbar2 = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src='https://evpa.eu.com/uploads/images/Trividend.jpg', height="30px")),
                        dbc.Col(dbc.NavbarBrand("Financial Dashboard Portfolio Trividend", className="ms-2",), width='auto'),
                    ],align="center",
                ),className="m-auto", style={"textDecoration": "none"}
            ),
        ],
    ),
    color="white",
)
######################################################################################################################
#! Body of tabs
######################################################################################################################
body1 = html.Div([
    dbc.Container(
        [
            navbar,
            dbc.Row(dbc.Col(html.H5('Algemene informatie posities', style={'text-align': 'center'}), width=12)),
            html.Hr(),
            dbc.Row(
                [
                    dbc.Col(html.Div(id='bedrijfsnaam'), width=6),
                    dbc.Col(html.Div(id='lening_tekst'), width=6, align='center'),
                ]),
            dbc.Row(
                [
                    dbc.Col(html.Div(id='participatie'), width=6),
                    dbc.Col(html.Div(id='lening_table'), width=6),
                ]),
            dbc.Row(
                [
                    dbc.Col(html.Div(id='geinvesteerd_bedrag'), width={"size": 6, "offset": 6}),
                ]),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(id='cijfer_table'),
                ]),
        ],
    )
])

body2 = html.Div(
    dbc.Container(
        [
            dbc.Row(dbc.Col(navbar2)),
            dbc.Row(dbc.Col(html.H5('Ratio informatie', style={'text-align': 'center'}), width=12)),
            html.Hr(),
            dbc.Row(dbc.Col(id='ratio_table'))
        ]
    )
)

body3 = html.Div(
    dbc.Container(
        [
            dbc.Row(dbc.Col(navbar2)),
            dbc.Row(dbc.Col(html.H5('Ratio Grafieken', style={'text-align': 'center'}), width=12)),
            html.Hr(),
            dbc.Row(dbc.Col(dcc.Graph(id='liquiditeitsgraph'))),
            dbc.Row(dbc.Col(dcc.Graph(id='rendabiliteitsgraph'))),
            dbc.Row(dbc.Col(dcc.Graph(id='structuurgraph'))),

        ]
    )
)
tabs = dbc.Tabs(
    [
        # dbc.Tab(body4, label='Market'),
        dbc.Tab(body1, label='Algemene informatie'),
        dbc.Tab(body2, label="Ratio's"),
        dbc.Tab(body3, label='Grafieken'),
    ]
)

app.layout = dbc.Container(tabs)

register_callbacks_info(app)
#######################################################################################################################

if __name__ == '__main__':
    app.run_server(debug=True)
