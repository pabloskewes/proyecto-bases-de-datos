from typing import List
import json

import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table
from dash.dependencies import Input, Output, State
import pandas as pd

from src.client import get_client
from src.logger import get_logger
from src.utils import fix_name
from src import ids
from src.dto import TrazadoDTO


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
                html.H5("Ida"),
                dbc.Container(
                    dbc.Row(
                        id=ids.TABLA_RUTA_IDA,
                        children=[],
                    )
                ),
            ]
        ),
    )
    regreso_container = dbc.Container(
        dbc.Row(
            [
                html.H5("Regreso"),
                dbc.Container(
                    dbc.Row(
                        id=ids.TABLA_RUTA_REGRESO,
                        children=[],
                    ),
                ),
            ]
        ),
    )
    separator = html.Div(
        className="vertical-separator",
        style={
            "border-right": "1px solid #ccc",
            "margin": "0 10px",
            "height": "100%",
        },
    )
    store_trazados = dcc.Store(id=ids.TRAZADOS_DATA_STORE)

    register_callbacks(app)

    return dbc.Container(
        dbc.Row(
            [
                title,
                dbc.Col(
                    [
                        ida_container,
                        separator,
                        regreso_container,
                    ],
                    width=6,
                    style={"display": "flex", "justify-content": "center"},
                ),
                store_trazados,
            ],
            className="detail-route-container",
        ),
    )


def build_trazado_button(trazado: TrazadoDTO, id_num: int) -> html.Li:
    return html.Li(
        fix_name(trazado.calle),
        id={"type": ids.TRAZADO_ITEM, "index": id_num},
        style={
            "text-decoration": "underline",
            "color": "blue",
            "cursor": "pointer",
            "list-style": "none",
        },
        # n_clicks=0,
    )


def register_callbacks(app: dash.Dash) -> None:
    @app.callback(
        Output(ids.DETALLE_RUTA_TITLE, "children"),
        Output(ids.TABLA_RUTA_IDA, "children"),
        Output(ids.TABLA_RUTA_REGRESO, "children"),
        Output(ids.TRAZADOS_DATA_STORE, "data"),
        Input(ids.RECORRIDO_DATA_STORE, "modified_timestamp"),
        State(ids.RECORRIDO_DATA_STORE, "data"),
        prevent_initial_call=True,
    )
    def update_detalle_ruta(
        _,
        recorrido_data: dict,
    ) -> List[html.Div]:
        if recorrido_data is None:
            return dash.no_update

        logger.log(f"recorrido_data: {recorrido_data}", tags=["DETALLE-RUTA"])

        nombre_recorrido = recorrido_data["nombre_recorrido"]
        detalle_ruta = client.get_detalle_ruta(
            region=recorrido_data["s_region"],
            folio=recorrido_data["s_folio"],
            nombre_recorrido=nombre_recorrido,
        )
        logger.log(f"detalle_ruta: {detalle_ruta}", tags=["DETALLE-RUTA"])

        title = html.H3(f"Detalle Ruta {fix_name(nombre_recorrido)}")
        item_id = 0
        ida_items = []
        regreso_items = []
        data = []
        for trazado in detalle_ruta.ida:
            ida_items.append(build_trazado_button(trazado, item_id))
            data.append(trazado.dict())
            item_id += 1
        for trazado in detalle_ruta.regreso:
            regreso_items.append(build_trazado_button(trazado, item_id))
            data.append(trazado.dict())
            item_id += 1

        ida = html.Ul(ida_items)
        regreso = html.Ul(regreso_items)

        return title, ida, regreso, data
