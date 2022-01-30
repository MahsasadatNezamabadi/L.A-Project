from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import pathlib
from app import app
from apps.getPrediction import get_pred

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()
#imgPath=PATH.joinpath("../images/four.jpg").resolve()
data = pd.read_csv(DATA_PATH.joinpath("dataForScatter.csv"))


schools=data["school_name"].unique()
label_school=[]
for l in schools:
    dict_label={"label":l,"value":l}
    label_school.append(dict_label)
first_school=label_school[0]["value"]
print(first_school)

layout=html.Div([
    html.H1("Second Page"),
    html.Span("Pick a school to see the prediction"),
    dcc.Dropdown(id="school",
                 options=label_school,
                 searchable=True,
                 clearable=False,
                 value=first_school
                 ),
    html.Div([
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
    )]),
    html.Div(id='slider-output'),
    html.Img(id="Pred"),
    html.Div(id="school_value")
])
#@app.callback(Output(component_id="school_value"), Input(component_id="school"))
@app.callback([Output(component_id="trees",component_property="value"),
               Output(component_id="crashes",component_property="value"),
               Output(component_id="pc",component_property="value"),
               Output(component_id="shootings",component_property="value"),
               Output(component_id="arrests",component_property="value"),
               Output(component_id="programs",component_property="value"),
               Output(component_id="bins",component_property="value")],
              Input(component_id= "school", component_property="value"))
def get_sliderValues(school):
    df=data[data["school_name"]==school]
    trees=df["trees"].to_list()[0]
    crashes=df["crashes"].to_list()[0]
    pc=df["pc"].to_list()[0]
    shootings=df["shootings"].to_list()[0]
    arrests=df["arrests"].to_list()[0]
    programms= df["programs"].to_list()[0]
    bins= df["bins"].to_list()[0]
    return trees,crashes,pc,shootings,arrests,programms,bins

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

@app.callback(Output(component_id="Pred",component_property="src"),[
    Input(component_id="trees",component_property="value"),Input(component_id="crashes",component_property="value"),
    Input(component_id="pc",component_property="value"), Input(component_id="shootings",component_property="value"),
    Input(component_id="arrests",component_property="value"), Input(component_id="programs",component_property="value"),
    Input(component_id="bins",component_property="value")
    ])

def get_Prediction(trees,crashes,pc,shootings,arrests,programs,bins):
    dict_feat={"trees":[trees],"crashes":[crashes],"pc":[pc],"shootings":[shootings],
               "arrests":[arrests],"programs":[programs],"bins":[bins]}

    feat=pd.DataFrame(data=dict_feat)
    pred=get_pred(feat)
    if pred[0] == 0:
        filename="zero.jpeg"
    elif pred[0]==1:
        filename="one.jpeg"
    elif pred[0]==2:
        filename="two.jpeg"
    elif pred[0]==3:
        filename="three.jpeg"
    elif pred[0]==4:
        filename="four.jpeg"
    fname = "/assets/"+filename

    print(pred)
    return fname

