from typing import List
import json

import dash
import dash_bootstrap_components as dbc
from dash import html, dash_table
from dash.dependencies import Input, Output, State, ALL
import pandas as pd

from src.client import get_client
from src.logger import get_logger
from src.utils import fix_name
from src import ids
from src.dto import VehicleDTO


logger = get_logger()
client = get_client()


COLUMN_NAMES = {
    "nombre_responsable": "Nombre Responsable",
    "patente": "Patente",
    "marca": "Marca",
    "modelo": "Modelo",
    "año_fabricacion": "Año Fabricación",
}


def render(app: dash.Dash) -> dbc.Container:
    title = html.Div(
        html.H3("Información Vehículos"),
        id=ids.VEHICLES_INFO_TITLE,
    )
    table = html.Div(
        id=ids.VEHICLES_INFO_CONTAINER,
        children=build_table([]),
    )

    register_callbacks(app)

    return dbc.Container(
        dbc.Row(
            [
                title,
                table,
            ]
        )
    )


def build_table(vehicles: List[VehicleDTO]) -> dash_table.DataTable:
    if not vehicles:
        return dash_table.DataTable(id=ids.TABLE_VEHICLES)

    records = [vehicle.dict() for vehicle in vehicles]
    data = pd.DataFrame.from_records(records)
    data["nombre_responsable"] = data["nombre_responsable"].apply(fix_name)

    table = dash_table.DataTable(
        id=ids.TABLE_VEHICLES,
        columns=[
            {"name": COLUMN_NAMES[column], "id": column} for column in data.columns
        ],
        data=data.to_dict("records"),
        style_cell_conditional=[
            {"if": {"column_id": "recorrido_data"}, "width": "0px", "display": "none"}
        ],
        style_header={"backgroundColor": "white", "fontWeight": "bold"},
        style_data={"whiteSpace": "normal", "height": "auto", "lineHeight": "15px"},
        style_table={"maxHeight": "500px", "overflowY": "scroll"},
        page_size=6,
    )

    return table


def register_callbacks(app: dash.Dash):
    @app.callback(
        Output(ids.VEHICLES_INFO_CONTAINER, "children"),
        Output(ids.VEHICLES_INFO_TITLE, "children"),
        Input({"type": ids.TRAZADO_ITEM, "index": ALL}, "n_clicks"),
        State(ids.TRAZADOS_DATA_STORE, "data"),
        prevent_initial_call=True,
    )
    def update_table(n_clicks, trazados_data):        
        triggered_id = dash.callback_context.triggered[0]["prop_id"].split(".")[0]
        index = int(json.loads(triggered_id)["index"])
        trazado = trazados_data[index]
        
        logger.log(f"triggered_id: {triggered_id}", tags=["VEHICLES-INFO"])
        logger.log(f"trazado: {trazado}", tags=["VEHICLES-INFO"])
        
        vehicles = client.get_vehicles(
            region=trazado["region"],
            comuna=trazado["comuna"],
            calle=trazado["calle"],
        )

        title = html.Div(
            html.H3(f"Vehículos en {fix_name(trazado['calle'])}"),
            id=ids.VEHICLES_INFO_TITLE,
        )
        table = build_table(vehicles)

        return table, title
