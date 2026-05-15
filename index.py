from dash import html, dcc
from dash.dependencies import Input, Output, State
from home import create_page_home
from app import app
from sqlalchemy import create_engine
import pandas as pd
from navbar import create_navbar
from datetime import date, timedelta
import os
import logging

server = app.server
app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    return create_page_home()

if __name__ == '__main__':

    log_path = os.path.abspath('App.log')
    logging.basicConfig(filename=log_path, level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s', filemode='a')

    app.run(debug=False)

    logging.info("*******************************\n********** DEMARRAGE DE L'APPLICATION ****************")