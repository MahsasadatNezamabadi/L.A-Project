from dash import dcc
from dash import html
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app

from apps import mlPart, ScatterDropDown

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dcc.Link('Scatter|', href='/apps/testScatter'),
        dcc.Link('ML', href='/apps/mlPart'),
    ], className="row"),
    html.Div(id='page-content', children=[])
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/testScatter':
        return ScatterDropDown.layout
    if pathname == '/apps/mlPart':
        return mlPart.layout
    else:
        return "404 Page Error! Please choose a link"


if __name__ == '__main__':
    app.run_server(debug=True)