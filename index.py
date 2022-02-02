from dash import dcc
from dash import html
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app

from apps import mlPart, ScatterDropDown, startPage

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dcc.Link('Discover the Data|', href='/apps/testScatter'),
        dcc.Link('Predict the Graduation Rate', href='/apps/mlPart'),
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
        return startPage.layout


if __name__ == '__main__':
    app.run_server(debug=True)