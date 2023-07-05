from pathlib import Path
import dash
from dash import html, dcc
import plotly.express as px
import pandas as pd
import geopandas as gpd

from src import ids
from src.logger import get_logger

logger = get_logger()
BASE_DIR = Path(__file__).parent.parent.parent.resolve()
regiones_path = BASE_DIR / "data" / "regiones.json"


@logger.wrap_func(tags=["CHILE-MAP"])
def get_chile_data(path: str) -> gpd.GeoDataFrame:
    """
    Get the Chile data
    Args:
        path (str): The path to the Chile data
    Returns:
        gpd.GeoDataFrame: The Chile data
    """
    logger.log("Getting Chile data...")
    gdf = (
        gpd.read_file(path)
        .set_index("codregion")
    )
    return gdf


def get_mock_data() -> pd.DataFrame:
    return pd.DataFrame({
        'codregion': list(range(1, 17)),
        'value': [1] * 16
    })

class ChileMap:
    def __init__(self, app: dash.Dash):
        self.app = app
        self.fig = None
        self.chile_data = get_chile_data(regiones_path)
        self._build_figure()

    @logger.wrap_func(tags=["CHILE-MAP"])
    def _build_figure(self):
        
        logger.log("Building Chile map...")
        mock_data = get_mock_data()
        fig = px.choropleth_mapbox(
            data_frame=mock_data,
            geojson=self.chile_data,
            locations='codregion',
            color='value',
            mapbox_style="open-street-map",
            center=dict(lat=-35, lon=-71),
            zoom=3,
            height=800,
            width=800,
            range_color=[0, 1],
            color_continuous_scale="blues",
        )
        
        fig.update_traces(
            marker_opacity=0.3
        )
        
        self.fig = fig
        
    def render(self) -> dash.html:
        """ Render the Chile map """
        return html.Div([
            dcc.Graph(
                id=ids.CHILE_MAP,
                figure=self.fig,
            )
        ])
