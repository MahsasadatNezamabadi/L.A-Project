import pandas as pd
import plotly
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
import dash
from dash.exceptions import PreventUpdate
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State

data = pd.read_csv("data/dataforscatter.csv")
data.drop(["dbn", "location", "demographic_category"], axis = 1, inplace = True)
#data = data.loc[:,["school_name", "borough", "trees", "crashes", "pc", "shootings", "arrests", "programs", "bins", "corhort_year", "total_grads_of_cohort"]]
data["total_grads_of_cohort"] = data["total_grads_of_cohort"].apply(np.ceil)
school_name = data["school_name"]
borough = data["borough"]
trees = data["trees"]
crashes = data["crashes"]
pc = data["pc"]
shootings = data["shootings"]
arrests = data["arrests"]
programs = data["programs"]
bins = data["bins"]
grades = data["total_grads_of_cohort"]
app = dash.Dash(__name__)


app.layout = html.Div([
    html.Div([dcc.Graph(id="scatterPlot")]),
    dcc.Dropdown(
        id="Borough",
        options=[
            {"label": "Bronx", "value": "Bronx"},
            {"label": "Brooklyn", "value": "Brooklyn"},
            {"label": "Manhatten", "value": "Manhatten"},
            {"label": "Queens", "value": "Queens"},
            {"label": "Staten Island", "value": "Staten Island"},
            {"label": "All", "value": "all"},
        ],
        value="Bronx",
        multi = True,
        searchable=True,
        placeholder="Please search"
    ),
    html.Div(id="Borough-output"),


    dcc.Dropdown(
        id="Filter",
        options=[
            {"label": "Trees", "value": "trees"},
            {"label": "Vehicle Crashes", "value": "crashes"},
            {"label": "Public Computer", "value": "pc"},
            {"label": "Shootings", "value": "shootings"},
            {"label": "Arrests", "value": "arrests"},
            {"label": "After School programs", "value": "programs"},
            {"label": "Recycling Bins", "value": "bins"}
        ],
        value="trees",
        disabled= False

    ),
    html.Div(id="Filter-output")
])
#    html.Div([
#        "Year",
#        dcc.Dropdown(id="Year", multi=True),
#    ]),


@app.callback(
    Output(component_id="scatterPlot",component_property="figure"),
    [Input(component_id="Borough", component_property="value"),Input(component_id="Filter",component_property="value")]
)
def build_graph(borough_choosen,filter):
    listBor=[]
    listBor.extend(borough_choosen)
    if "all" in borough_choosen:
        df=data
    else:
        df=data[data["borough"].isin(listBor)]
    print(listBor)
    print(filter)
    fig = px.scatter(df, x=filter, y="total_grads_of_cohort",
                     hover_data=["school_name", "borough"])
    return fig



if __name__ == "__main__":
    app.run_server(debug=True)