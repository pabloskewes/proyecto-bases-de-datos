from pathlib import Path

from flask import Flask
import dash
import dash_bootstrap_components as dbc

from src.components import layout


BASE_DIR = Path(__file__).parent.resolve()
ASSETS_PATH = BASE_DIR / "assets"

server = Flask(__name__)
app = dash.Dash(
    __name__,
    server=server,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    assets_folder=ASSETS_PATH,
)

app.layout = layout.render(app)


if __name__ == "__main__":
    server.run(debug=True, host="0,0,0,0", port=8090)
    # import gunicorn
    
    # gunicorn.run(server, port=8090)
