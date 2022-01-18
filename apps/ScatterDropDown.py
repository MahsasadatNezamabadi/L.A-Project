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
from app import app
import pathlib

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

data = pd.read_csv(DATA_PATH.joinpath("dataForScatter.csv"))
#data = pd.read_csv("datasets/dataforscatter.csv")

#datasets = datasets.loc[:,["school_name", "borough", "trees", "crashes", "pc", "shootings", "arrests", "programs", "bins", "corhort_year", "total_grads_of_cohort"]]
data["total_grads_of_cohort"] = data["total_grads_of_cohort"].apply(float)
#app = dash.Dash(__name__)
#can be hopefully deleted after changing the data
list_loc = data["location"].to_list()
list_loc = [x.split(",") for x in list_loc]
list_lat=[x[0] for x in list_loc]
list_lat=[x.split("(") for x in list_lat]
list_lat=[float(x[1]) for x in list_lat]
data["latitude"]=list_lat
list_long=[x[1] for x in list_loc]
list_long=[x.split(")") for x in list_long]
list_long=[float(x[0]) for x in list_long]
data["longitude"]=list_long

layout = html.Div([
    html.H1("NY City school explorer"),
    html.Div([html.Span("Map of New York City & the schools"),
              dcc.Graph(id="map", figure={})]),
    html.Div([html.Span("See a Scatterplot for the different features & schools"),dcc.Graph(id="scatterPlot", figure={})]),
    dcc.Dropdown(
        id="Borough",
        options=[
            {"label": "Bronx", "value": "Bronx"},
            {"label": "Brooklyn", "value": "Brooklyn"},
            {"label": "Manhattan", "value": "Manhattan"},
            {"label": "Queens", "value": "Queens"},
            {"label": "Staten Island", "value": "Staten Island"},
            {"label": "All", "value": "all"},
        ],
        value=["Bronx"],
        multi = True,
        searchable=True,
        placeholder="Please search"
    ),
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

    )
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

@app.callback(
    Output(component_id="map",component_property="figure"),
    Input(component_id="Borough",component_property="value"))
def get_map(borough_chs):
    #df =data
    #df["total_grads_of_cohort"]=df["total_grads_of_cohort"].apply(str)
    fig = px.scatter_mapbox(data, lat="latitude", lon="longitude", hover_name="school_name",
                            hover_data=["total_grads_of_cohort" ],color_discrete_sequence=["fuchsia"], zoom=10, height=700)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig



