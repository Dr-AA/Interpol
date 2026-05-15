from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
from datetime import date

def create_navbar():
    navbar = html.Div([
        dbc.Row(
            [
                dbc.Col(
                    html.Img(
                        src=r'assets/Logo-Bleu-V2.png',
                        alt='image',
                        className='img-fluid',
                        style={'max-width': '110px'}
                    ),
                    width=2,
                    className='d-flex align-items-center'
                ),
                dbc.Col(
                    dbc.NavbarSimple(
                        brand=html.Span(["LEMAN", html.Sup("d")," - Nos sites en optimisation énergétique"]),
                        brand_href="/",
                        sticky="top",
                        color="#1f388b",
                        dark=True,
                        className='p-2',
                        style={
                            "height":'40px',
                        }

                    ),
                    width=10
                )
            ],
            align='center',
            className='g-0'
        )
    ])
    return navbar

