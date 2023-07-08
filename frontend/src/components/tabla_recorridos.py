from typing import List
import json

import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash import dash_table, html, dcc
import pandas as pd

from src.client import get_client
from src.logger import get_logger
from src.utils import fix_name
from src import ids
from src.dto import RecorridoDTO

logger = get_logger()
client = get_client()


COLUMN_NAMES = {
    "nombre_recorrido": "Nombre Recorrido",
    "lugar_origen": "Lugar Origen",
    "lugar_destino": "Lugar Destino",
    "s_folio": "Folio Servicio",
    "s_region": "Region Servicio",
}


def render(app: dash.Dash) -> html.Div:
    title = html.Div(
        html.H3("Recorridos Disponibles"),
        id=ids.TABLA_RECORRIDOS_TITLE,
    )
    alert = dbc.Alert(
        "Por favor, seleccione todas las opciones",
        id=ids.ALERT_RECORRIDOS,
        color="danger",
        dismissable=True,
        is_open=False,
    )
    table = html.Div(
        id=ids.TABLA_RECORRIDOS_CONTAINER,
        children=build_table([]),
    )

    store = dcc.Store(id=ids.RECORRIDO_DATA_STORE)

    register_callbacks(app)

    return dbc.Container(
        dbc.Row(
            dbc.Col(
                html.Div(
                    children=[
                        title,
                        alert,
                        table,
                        store,
                    ],
                )
            )
        )
    )


def build_table(recorridos: List[RecorridoDTO]) -> dash_table.DataTable:
    if not recorridos:
        return dash_table.DataTable(id=ids.TABLA_RECORRIDOS)

    records = [recorrido.dict() for recorrido in recorridos]
    data = pd.DataFrame.from_records(records)
    name_columns = ["nombre_recorrido", "lugar_origen", "lugar_destino"]
    data[name_columns] = data[name_columns].applymap(fix_name)

    # Adding a hidden column to store the RecorridoDTO object
    hidden_column = {"name": "recorrido_data", "id": "recorrido_data"}
    columns = [{"name": COLUMN_NAMES[i], "id": i} for i in data.columns]
    columns.append(hidden_column)

    data["recorrido_data"] = [recorrido.json() for recorrido in recorridos]

    table = dash_table.DataTable(
        id=ids.TABLA_RECORRIDOS,
        columns=columns,
        data=data.to_dict("records"),
        style_cell_conditional=[
            {"if": {"column_id": "recorrido_data"}, "width": "0px", "display": "none"}
        ],
        style_header={"backgroundColor": "white", "fontWeight": "bold"},
        style_data={"whiteSpace": "normal", "height": "auto", "lineHeight": "15px"},
        style_table={"maxHeight": "500px", "overflowY": "scroll"},
    )

    return table


def register_callbacks(app: dash.Dash):
    @app.callback(
        Output(ids.TABLA_RECORRIDOS_CONTAINER, "children"),
        Output(ids.TABLA_RECORRIDOS_TITLE, "children"),
        Output(ids.ALERT_RECORRIDOS, "is_open"),
        Input(ids.SEARCH_RECORRIDOS_BUTTON, "n_clicks"),
        State(ids.FROM_REGION_DROPDOWN, "value"),
        State(ids.FROM_COMUNA_DROPDOWN, "value"),
        State(ids.TO_REGION_DROPDOWN, "value"),
        State(ids.TO_COMUNA_DROPDOWN, "value"),
        prevent_initial_call=True,
    )
    def update_table(n_clicks, from_region, from_comuna, to_region, to_comuna):
        if n_clicks is None:
            return dash.no_update

        alert_is_open = False

        if (
            from_region is None
            or from_comuna is None
            or to_region is None
            or to_comuna is None
        ):
            logger.log("No se han seleccionado todas las opciones")
            logger.log(
                f"{from_region = } | {from_comuna = } | {to_region = } | {to_comuna = }"
            )
            alert_is_open = True
            return dash.no_update, dash.no_update, alert_is_open

        recorridos = client.get_recorridos(
            from_region, from_comuna, to_region, to_comuna
        )
        table = build_table(recorridos)

        if not recorridos:
            table = dbc.Alert(
                "No se encontraron recorridos disponibles",
                color="warning",
                dismissable=True,
            )

        title = f"Recorridos disponibles desde {from_comuna} a {to_comuna}"
        return table, title, alert_is_open

    @app.callback(
        Output(ids.RECORRIDO_DATA_STORE, "data"),
        Input(ids.TABLA_RECORRIDOS, "active_cell"),
        State(ids.TABLA_RECORRIDOS, "data"),
        prevent_initial_call=True,
    )
    def store_recorrido(active_cell, data):
        if active_cell is None:
            return dash.no_update

        row = active_cell["row"]
        recorrido_data = data[row]["recorrido_data"]
        return json.loads(recorrido_data)
