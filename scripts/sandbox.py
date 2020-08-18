import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

# create app object using the external stylesheet
app = dash.Dash(__name__, external_stylesheets = external_stylesheets)

# create data
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

# create a plotly express bar chart object
fig = px.bar(df, x = 'Fruit', y = 'Amount', color = 'City', barmode = 'group')

fig.update_layout(
    plot_bgcolor = colors['background'], 
    paper_bgcolor = colors['background'],
    font_color = colors['text']
    )

# create a layout that is a div, containing a h1, div and graph
app.layout = html.Div(style = {'backgroundColor':colors['background']}, children = [

    html.H1(style = {'textAlign': 'center', 'color': colors['text']}, children = 'Hello Dash'),
    html.Div(style = {'textAlign': 'center', 'color': colors['text']}, children = '''Dash: A web app framework for Python'''),
    dcc.Graph(id = 'example-graph', figure = fig)

])

# launch the app
if __name__ == '__main__':
    app.run_server(debug = True)
