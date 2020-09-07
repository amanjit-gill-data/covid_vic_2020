import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

df = pd.read_csv('../data/all_dates.csv')
df.set_index('lga', inplace = True)

app = dash.Dash(__name__)

print(len(df.columns))
print(len(df.loc[['CASEY', 'MELBOURNE']]))
print(df.loc[['CASEY', 'MELBOURNE']])

fig1 = px.line(x = df.columns, y = df.loc['CASEY'])

app.layout = html.Div([

    html.H1("Daily Cases by LGA"),

    dcc.Graph(figure = fig1),

    dcc.Input(id = 'lga-input', value = 'MELBOURNE', type = 'text'),

    dcc.Graph(id = 'out-graph')
])

@app.callback(
    Output('out-graph', 'figure'),
    [Input('lga-input', 'value')]
)

def create_graph(lga_name):
    return px.line(x = df.columns, y = df.loc[lga_name])

if __name__ == '__main__':
    app.run_server(debug=True)