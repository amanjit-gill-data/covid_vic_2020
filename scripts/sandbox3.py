import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([

    html.Label('Multi-select dropdown'),

    dcc.Dropdown(
        options = [
            {'label': 'Banyule', 'value': 'Ban'},
            {'label': 'Casey', 'value': 'Cas'},
            {'label': 'Melbourne', 'value': 'Mel'}
        ],
        value = ['Cas'],
        multi = True
    ),

    html.Label('Slider'),

    dcc.Slider(
        min=0,
        max=5,
        marks={i:str(i) for i in range(1, 6)},
        value=3
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)