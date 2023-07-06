import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash import dash_table, html
import pandas as pd

from src.mock_client import get_client
from src.logger import get_logger
from src import ids

logger = get_logger()
client = get_client()


class TablaRecorridos:
    def __init__(self, app: dash.Dash):
        self.app = app
        self.data: pd.DataFrame = None
        self.table = None
        self._register_callbacks()

    def _update_data(
        self, from_region: int, from_comuna: str, to_region: int, to_comuna: str
    ):
        recorridos = client.get_recorridos(
            from_region, from_comuna, to_region, to_comuna
        )
        self.data = pd.DataFrame.from_records(recorridos["recorridos"])
        
    def _build_table(
        self, from_region: int, from_comuna: str, to_region: int, to_comuna: str
    ) -> None:
        self._update_data(from_region, from_comuna, to_region, to_comuna)
        self.table = dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in self.data.columns],
            data=self.data.to_dict('records'),
            style_cell={'textAlign': 'left'},
            style_header={
                'backgroundColor': 'white',
                'fontWeight': 'bold'
            },
            style_data={
                'whiteSpace': 'normal',
                'height': 'auto',
                'lineHeight': '15px'
            },
            style_table={
                'maxHeight': '500px',
                'overflowY': 'scroll'
            }
        )
    
    def render(self):
        return dbc.Container(
            dbc.Row(
                dbc.Col(
                    html.Div(
                        children=[
                            html.Div(html.H3("Recorridos Disponibles"), id=ids.TABLA_RECORRIDOS_TITLE),
                            html.Div(id=ids.TABLA_RECORRIDOS),
                        ],
                    )
                )
            )
        )
    
    @logger.wrap_func(tags=["TABLA-RECORRIDOS"])
    def _register_callbacks(self):
        @self.app.callback(
            Output(ids.TABLA_RECORRIDOS, "children"),
            Output(ids.TABLA_RECORRIDOS_TITLE, "children"),
            Input(ids.SEARCH_RECORRIDOS_BUTTON, "n_clicks"),
            State(ids.FROM_REGION_DROPDOWN, "value"),
            State(ids.FROM_COMUNA_DROPDOWN, "value"),
            State(ids.TO_REGION_DROPDOWN, "value"),
            State(ids.TO_COMUNA_DROPDOWN, "value"),
        )
        def update_table(n_clicks, from_region, from_comuna, to_region, to_comuna):
            if n_clicks is None:
                return dash.no_update
            if from_region is None or from_comuna is None or to_region is None or to_comuna is None:
                logger.log("No se han seleccionado todas las opciones")
                logger.log(f"{from_region = } | {from_comuna = } | {to_region = } | {to_comuna = }")
                return dash.no_update
            
            self._update_data(from_region, from_comuna, to_region, to_comuna)
            self._build_table(from_region, from_comuna, to_region, to_comuna)
            
            title = f"Recorridos disponibles desde {from_comuna} a {to_comuna}"
            return self.table, title
        