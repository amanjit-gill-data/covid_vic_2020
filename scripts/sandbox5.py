import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

df = pd.read_csv('../data/all_dates.csv')
df.set_index('lga', inplace = True)

app = dash.Dash(__name__)

lga_keys = df.index.to_list()
lga_values = [key.upper() for key in lga_keys]
lga_dict = dict(zip(lga_keys, lga_values))

print(lga_dict)

app.layout = html.Div([

    html.H1("Daily Cases for Selected LGAs"),

    dcc.Dropdown(
        id = 'lga-input',
        options = [{'label': 'Casey', 'value': 'CASEY'},
                    {'label': 'Banyule', 'value': 'BANYULE'},
                    {'label': 'Wyndham', 'value': 'WYNDHAM'}],
        value = ['CASEY'],
        multi = True
    ),

    dcc.Graph(id = 'out-graph')
])

@app.callback(
    Output('out-graph', 'figure'),
    [Input('lga-input', 'value')]
)

def create_graph(lga_names):
    series_list = [df.loc[lga] for lga in lga_names]
    return px.line(x = df.columns, y = series_list)

if __name__ == '__main__':
    app.run_server(debug=True)