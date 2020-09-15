import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import math

app = dash.Dash(__name__)

df = pd.read_csv('data/all_dates.csv')
df.set_index('lga', inplace = True)

# function that is called every time the page is reloaded
# this function is used rather than just doing app.layout = html.Div(etc),
# as that won't load the updated df until the app is stopped and restarted on the server

def serve_layout():

    # reload df in case it has been updated since the app started running

    df = pd.read_csv('data/all_dates.csv')
    df.set_index('lga', inplace = True)

    # create dictionary of lga labels and values
    # to be used in the multi-select dropdown

    lga_keys = df.index.to_list()
    lga_dicts = []
    for lga in lga_keys:
        lga_dicts.append(dict(zip(['label', 'value'], [lga, lga]))) # keys and values are the same

    # return layout of app
    # heading, then videos, then another heading, then multi-select dropdown, then graph

    return html.Div([

        html.H2("Daily Active Cases in Victorian LGAs"),

        html.Div(
            children = [
                html.Video(
                    children = [
                        html.Source(src = '/assets/videos/melb.mp4', type = 'video/mp4'),
                        "Video not supported"
                    ],
                    width = '45%',
                    autoPlay = False,
                    controls = True
                ),
                html.Video(
                    children = [
                        html.Source(src = '/assets/videos/all_vic.mp4', type = 'video/mp4'),
                        "Video not supported"
                    ],
                    width = '45%',
                    autoPlay = False,
                    controls = True
                )
            ],
            className = 'video-row'
        ),

        html.H2("Compare LGAs"),

        dcc.Dropdown(
            id = 'lga-input',
            options = lga_dicts,
            value = ['MELBOURNE'],
            multi = True
        ),

        dcc.Graph(id = 'out-graph')
    ])

# set up callback
# when the dropdown 'lga-input' is updated, the graph 'out-graph' will be updated

@app.callback(
    Output('out-graph', 'figure'),
    [Input('lga-input', 'value')]
)

# this function is called whenever the dropdown is updated
# if there is at least one LGA selected, the row for each LGA is extracted from the df (as a series)
# and put into a list of series, then each series is plotted onto the figure
# if there are no LGAs selected, an empty graph is returned
def create_graph(lga_names):

    fig = go.Figure()

    if (len(lga_names) > 0):
        series_list = [df.loc[lga] for lga in lga_names]
        for series in series_list:
            fig.add_trace(go.Scatter(
                x = df.columns, 
                y = series, 
                mode = 'lines', 
                name = series.name,
                hovertemplate = '<b>Date: %{x}, Active Cases: %{y}</b>'
            ))
        max_yval = max([series.max() for series in series_list])
        fig.update_yaxes(range = [0, math.ceil(max_yval/100)*100]) # round y-axis up to next 100
    else:
        fig.add_trace(go.Scatter(
            x = df.columns,
            y = [0]*len(df.columns),
            hoverinfo = 'skip'
        ))
        fig.update_yaxes(range = [0, 10])

    fig.update_xaxes(tick0 = '2020-07-01', dtick = 'M1', tickformat = '%d %b')
    fig.update_layout(
        legend = dict(yanchor = 'top', y = 0.99, xanchor = 'left', x = 0.01),
        xaxis_title = '<b>Date</b>',
        yaxis_title = '<b>Active Cases</b>',
        font_family = 'Calibri',
        font_size = 14
    )
    return fig

app.layout = serve_layout

if __name__ == '__main__':
    app.run_server(debug=True)