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


data["avg_perc Grads"] = data["avg_perc Grads"].apply(float)
data["avg_perc Grads"] = data["avg_perc Grads"].round()

data["latitude"]=data["latitude"].apply(float)

data["longitude"]=data["longitude"].apply(float)

layout = html.Div([
    html.H1("NY City school explorer"),
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

    ),
    html.Div([
              dcc.Graph(id="map", figure={},style={"display":"inline-block","width":"50%"}),
              dcc.Graph(id="scatterPlot", figure={},style={"display":"inline-block", "width":"50%"})])

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
    fig = px.scatter(df, x=filter, y="avg_perc Grads",
                     hover_data=["school_name", "borough"],
                     labels={"avg_perc Grads":"Average Graduation Rate in Percentage"})
    return fig

@app.callback(
    Output(component_id="map",component_property="figure"),
    Input(component_id="Borough",component_property="value"))

def get_map(borough_chosen):
    listBor = []
    listBor.extend(borough_chosen)
    if "all" in listBor:
        df = data
        zoom = 9.5
    else:
        df = data[data["borough"].isin(listBor)]
        zoom = 10


    fig = px.scatter_mapbox(df, lat="latitude", lon="longitude",
                            hover_name="school_name", hover_data=["avg_perc Grads"],
                            color_discrete_sequence=["fuchsia"], zoom=zoom)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig  # component_property of output




