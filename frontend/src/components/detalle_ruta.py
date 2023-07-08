from typing import List

import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output, State

from src.client import get_client
from src.logger import get_logger
from src.utils import fix_name
from src import ids
from src.dto import DetalleRutaDTO, RecorridoDTO


logger = get_logger()
client = get_client()


def build_calle(calle: str) -> html.Div:
    return html.Div(
        [
            html.H6(calle, hidden=True),
            html.Li(
                fix_name(calle),
                style={
                    "text-decoration": "underline",
                    "color": "blue",
                    "cursor": "pointer",
                    "list-style": "none",
                },
            ),
        ]
    )


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
                html.H5("Regreso"),
                dbc.Container(
                    dbc.Row(
                        id=ids.DETALLE_RUTA_REGRESO,
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

    register_callbacks(app)

    return dbc.Container(
        dbc.Row(
            [
                title,
                dbc.Col(
                    [
                        # separator,
                        ida_container,
                        separator,
                        regreso_container,
                        separator,
                    ],
                    width=6,
                    style={"display": "flex"},
                ),
            ],
        ),
    )


@logger.wrap_func(tags=["DETALLE-RUTA"])
def register_callbacks(app: dash.Dash) -> None:
    @app.callback(
        Output(ids.DETALLE_RUTA_TITLE, "children"),
        Output(ids.DETALLE_RUTA_IDA, "children"),
        Output(ids.DETALLE_RUTA_REGRESO, "children"),
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

        logger.log(f"recorrido_data: {recorrido_data}")

        nombre_recorrido = recorrido_data["nombre_recorrido"]
        detalle_ruta = client.get_detalle_ruta(
            region=recorrido_data["s_region"],
            folio=recorrido_data["s_folio"],
            nombre_recorrido=nombre_recorrido,
        )
        logger.log(f"detalle_ruta: {detalle_ruta}")

        title = html.H3(f"Detalle Ruta {fix_name(nombre_recorrido)}")
        ida = [build_calle(calle.nombre) for calle in detalle_ruta.ida]
        regreso = [build_calle(calle.nombre) for calle in detalle_ruta.regreso]

        return title, ida, regreso
