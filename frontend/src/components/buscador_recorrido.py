from dash import html, dcc, Dash
import dash_bootstrap_components as dbc

from src import ids


regions = [
    {'label': 'Región Metropolitana', 'value': '13'},
    {'label': 'Arica y Parinacota', 'value': '15'},
    {'label': 'Tarapacá', 'value': '1'},
    {'label': 'Antofagasta', 'value': '2'},
    {'label': 'Atacama', 'value': '3'},
    {'label': 'Coquimbo', 'value': '4'},
    {'label': 'Valparaíso', 'value': '5'},
    {'label': 'O’Higgins', 'value': '6'},
    {'label': 'Maule', 'value': '7'},
    {'label': 'Ñuble', 'value': '16'},
    {'label': 'Biobío', 'value': '8'},
    {'label': 'Araucanía', 'value': '9'},
    {'label': 'Los Ríos', 'value': '14'},
    {'label': 'Los Lagos', 'value': '10'},
    {'label': 'Aysén', 'value': '11'},
    {'label': 'Magallanes', 'value': '12'},
]


def render(app: Dash) -> html.Div:
    from_region_dropdown = dcc.Dropdown(
        id=ids.FROM_REGION_DROPDOWN,
        options=regions,
        value='13',
        placeholder='Seleccione una región',
    )
    
    from_city_dropdown = dcc.Dropdown(
        id=ids.FROM_CITY_DROPDOWN,
        options=[],
        value='',
        placeholder='Seleccione una ciudad',
    )
    
    to_region_dropdown = dcc.Dropdown(
        id=ids.TO_REGION_DROPDOWN,
        options=regions,
        value='13',
        placeholder='Seleccione una región',
    )
    
    to_city_dropdown = dcc.Dropdown(
        id=ids.TO_CITY_DROPDOWN,
        options=[],
        value='',
        placeholder='Seleccione una ciudad',
    )
         
    
    return html.Div(
        dbc.Row([
            dbc.Col([
                html.H3('Desde'),
                from_region_dropdown,
                from_city_dropdown,
            ]),
            dbc.Col([
                html.H3('Hasta'),
                to_region_dropdown,
                to_city_dropdown,
            ]),
        ])
    )
         
    
        