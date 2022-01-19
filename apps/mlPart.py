from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import pathlib
from app import app

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

data = pd.read_csv(DATA_PATH.joinpath("dataForScatter.csv"))

schools=data["school_name"].unique()
label_school=[]
for l in schools:
    dict_label={"label":l,"value":l}
    label_school.append(dict_label)

layout=html.Div([
    html.H1("Second Page"),
    html.Span("Pick a school to see the prediction"),
    dcc.Dropdown(id="school",
                 options=label_school,
                 searchable=True),
    html.Span("Pick the number of Features for the Machine Learning Model"),
    html.Span("Number of trees"),
    dcc.Slider(
        id="trees",
        min=0,
        max=data["trees"].max(),
        step=1,
        value=10,
    ),
    html.Span("Number of Vehicle crashes"),
    dcc.Slider(
        id="crashes",
        min=0,
        max=data["crashes"].max(),
        step=1,
        value=10,
    ),
    html.Span("Number of Public computers"),
    dcc.Slider(
        id="pc",
        min=0,
        max=data["pc"].max(),
        step=1,
        value=10,
    ),
    html.Span("Number of Shootings"),
    dcc.Slider(
        id="shootings",
        min=0,
        max=data["shootings"].max(),
        step=1,
        value=10,
    ),
    html.Span("Number of arrests"),
    dcc.Slider(
        id="arrests",
        min=0,
        max=data["arrests"].max(),
        step=1,
        value=10,
    ),
    html.Span("Number of After School Programs"),
    dcc.Slider(
        id="programs",
        min=0,
        max=data["programs"].max(),
        step=1,
        value=10,
    ),
    html.Span("Number of Public Recycling Bins"),
    dcc.Slider(
        id="bins",
        min=0,
        max=data["bins"].max(),
        step=1,
        value=10,
    ),
    html.Div(id='slider-output')
])

@app.callback(Output(component_id="slider-output",component_property="children"),[
    Input(component_id="trees",component_property="value"),Input(component_id="crashes",component_property="value"),
    Input(component_id="pc",component_property="value"), Input(component_id="shootings",component_property="value"),
    Input(component_id="arrests",component_property="value"), Input(component_id="programs",component_property="value"),
    Input(component_id="bins",component_property="value")
    ])

def get_sliderOutput(trees,crashes,pc,shootings,arrests,programs,bins):
    res_str=""
    res_str = res_str+'You have selected "{}" trees'.format(trees)
    res_str = res_str + 'You have selected "{}" crashes '.format(crashes)
    res_str = res_str + 'You have selected "{}" pc '.format(pc)
    res_str = res_str + 'You have selected "{}" shootings '.format(shootings)
    res_str = res_str + 'You have selected "{}" arrests '.format(arrests)
    res_str = res_str + 'You have selected "{}" programs '.format(programs)
    res_str = res_str + 'You have selected "{}" bins'.format(bins)
    return res_str

