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
lga_dicts = []
for lga in lga_keys:
    lga_dicts.append(dict(zip(['label', 'value'], [lga, lga])))

app.layout = html.Div([

    html.H1("Daily Cases for Selected LGAs"),

    dcc.Dropdown(
        id = 'lga-input',
        options = lga_dicts,
        value = ['MELBOURNE'],
        multi = True
    ),

    dcc.Graph(id = 'out-graph')
])

@app.callback(
    Output('out-graph', 'figure'),
    [Input('lga-input', 'value')]
)

def create_graph(lga_names):

    if (len(lga_names) > 0):
        series_list = [df.loc[lga] for lga in lga_names]
        max_yval = max([series.max() for series in series_list])
        fig = px.line(
            x = df.columns,
            y = series_list, 
            range_y = [0, max_yval+10],
            labels = {'x': 'Date', 'value': 'Active Cases'}
        )
    else:
        fig = px.line(
            x = df.columns,
            y = [0]*len(df.columns),
            range_y= [0, 10],
            labels = {'x': 'Date', 'y': 'Active Cases'}
        )
    fig.update_xaxes(tick0 = '2020-07-01', dtick = 'M1')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)