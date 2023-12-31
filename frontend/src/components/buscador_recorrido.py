from typing import List, Dict

from dash import html, dcc, Dash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from src import ids
from src.dto import ComunaDTO
from src.logger import get_logger
from src.client import get_client


logger = get_logger()
client = get_client()


regions = [
    {"label": "Región Metropolitana", "value": 13},
    {"label": "Arica y Parinacota", "value": 15},
    {"label": "Tarapacá", "value": 1},
    {"label": "Antofagasta", "value": 2},
    {"label": "Atacama", "value": 3},
    {"label": "Coquimbo", "value": 4},
    {"label": "Valparaíso", "value": 5},
    {"label": "O’Higgins", "value": 6},
    {"label": "Maule", "value": 7},
    {"label": "Ñuble", "value": 16},
    {"label": "Biobío", "value": 8},
    {"label": "Araucanía", "value": 9},
    {"label": "Los Ríos", "value": 14},
    {"label": "Los Lagos", "value": 10},
    {"label": "Aysén", "value": 11},
    {"label": "Magallanes", "value": 12},
]


def communes_to_options(communes: List[ComunaDTO]) -> List[Dict[str, str]]:
    return [{"label": comuna.nombre, "value": comuna.nombre} for comuna in communes]


def render(app: Dash) -> html.Div:
    from_region_dropdown = dcc.Dropdown(
        id=ids.FROM_REGION_DROPDOWN,
        options=regions,
        value="13",
        placeholder="Seleccione una región",
    )

    from_comuna_dropdown = dcc.Dropdown(
        id=ids.FROM_COMUNA_DROPDOWN,
        options=[],
        value=None,
        placeholder="Seleccione una ciudad",
    )

    to_region_dropdown = dcc.Dropdown(
        id=ids.TO_REGION_DROPDOWN,
        options=regions,
        value="13",
        placeholder="Seleccione una región",
    )

    to_comuna_dropdown = dcc.Dropdown(
        id=ids.TO_COMUNA_DROPDOWN,
        options=[],
        value=None,
        placeholder="Seleccione una ciudad",
    )

    search_button = dbc.Button(
        "Buscar recorridos",
        id=ids.SEARCH_RECORRIDOS_BUTTON,
        color="primary",
        className="mr-1",
        n_clicks=0,
    )

    register_callbacks(app)

    return html.Div(
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H3("Desde"),
                        from_region_dropdown,
                        from_comuna_dropdown,
                    ]
                ),
                dbc.Col(
                    [
                        html.H3("Hasta"),
                        to_region_dropdown,
                        to_comuna_dropdown,
                    ]
                ),
                search_button,
            ],
        )
    )


@logger.wrap_func(tags=["BUSCADOR-RECORRIDOS"])
def update_dropdown(region: int) -> List[Dict[str, str]]:
    comunas = client.get_comunas(region=region)
    return communes_to_options(comunas)


@logger.wrap_func(tags=["BUSCADOR-RECORRIDOS"])
def register_callbacks(app: Dash):
    app.callback(
        Output(ids.FROM_COMUNA_DROPDOWN, "options"),
        Input(ids.FROM_REGION_DROPDOWN, "value"),
    )(update_dropdown)

    app.callback(
        Output(ids.TO_COMUNA_DROPDOWN, "options"),
        Input(ids.TO_REGION_DROPDOWN, "value"),
    )(update_dropdown)
