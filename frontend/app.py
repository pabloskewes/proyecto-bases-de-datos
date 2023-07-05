import dash
import dash_bootstrap_components as dbc

from src.components import layout


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


app.title = "Parques Vehiculares"
app.layout = layout.render(app)


if __name__ == "__main__":
    app.run_server(port=8090, debug=True)
