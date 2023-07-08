from typing import List

import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output, State

from src.client import get_client
from src.logger import get_logger
from src import ids
from src.dto import DetalleRutaDTO


logger = get_logger()
client = get_client()


def render(app: dash.Dash) -> dbc.Container:
    title = html.Div(
        html.H3("Detalle Ruta"),
        id=ids.DETALLE_RUTA_TITLE,
    )
    ida_container = dbc.Container(
        dbc.Row(
            [
                html.H4("Ida"),
                dbc.Container(
                    dbc.Row(
                        id=ids.DETALLE_RUTA_IDA,
                        children=[],
                    )
                ),
            ]
        ),
    )
    regreso_container = dbc.Container(
        dbc.Row(
            [
                html.H4("Regreso"),
                dbc.Container(
                    dbc.Row(
                        id=ids.DETALLE_RUTA_REGRESO,
                        children=[],
                    ),
                ),
            ]
        ),
    )

    return dbc.Container(
        dbc.Row(
            [
                title,
                dbc.Col(
                    [
                        ida_container,
                        regreso_container,
                    ]
                ),
            ]
        ),
    )
