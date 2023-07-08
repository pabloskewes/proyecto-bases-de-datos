from pathlib import Path

import dash
import dash_bootstrap_components as dbc

from src.components import layout


BASE_DIR = Path(__file__).parent.resolve()
ASSETS_PATH = BASE_DIR / "assets"

app = dash.Dash(
    __name__, external_stylesheets=[dbc.themes.BOOTSTRAP], assets_folder=ASSETS_PATH
)

app.layout = layout.render(app)


if __name__ == "__main__":
    app.run_server(port=8090, debug=True)
