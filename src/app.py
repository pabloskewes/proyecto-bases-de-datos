import dash
from dash import html, dcc


# Create the Dash app
app = dash.Dash(__name__)

# Define the layout
app.layout = html.Div(
    children=[
        html.H1('PUDIN'),
        dcc.Dropdown(
            id='dropdown',
            options=[
                {'label': 'Option 1', 'value': 'option1'},
                {'label': 'Option 2', 'value': 'option2'},
                {'label': 'Option 3', 'value': 'option3'}
            ],
            value='option1'
        ),
        dcc.Input(
            id='input',
            type='text',
            placeholder='Enter text...'
        )
    ]
)

# Run the app
if __name__ == '__main__':
    app.run_server(port=8090, debug=True)