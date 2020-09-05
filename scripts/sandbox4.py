import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H6("Change value to see callbacks in action"),
    html.Div(["Input: ", dcc.Input(id = 'text-input', value = 'initial value', type = 'text')]),
    html.Br(),
    html.Div(id = 'text-output'),

    dcc.Graph(id = 'graph-with-slider'),
    dcc.Slider(
        id = 'year-slider', 
        min = df['year'].min(),
        max = df['year'].max(),
        value = df['year'].min(),
        marks = {str(i): str(i) for i in df['year'].unique()},
        step = None
    )
])

@app.callback(
    [Output('text-output', 'children'),
    Output('graph-with-slider', 'figure')],
    [Input('text-input', 'value'),
    Input('year-slider', 'value')]
)
def update_output_div_and_graph(input_text, input_year):

    filtered_df = df[df.year == input_year]

    fig = px.scatter(filtered_df, x="gdpPercap", y="lifeExp", 
                     size="pop", color="continent", hover_name="country", 
                     log_x=True, size_max=55)

    fig.update_layout(transition_duration=500)

    return 'Output: {}'.format(input_text), fig

if __name__ == '__main__':
    app.run_server(debug=True)