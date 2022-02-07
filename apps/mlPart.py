from dash import dcc, no_update
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import pathlib
from app import app
from apps.getPrediction import get_pred
import dash_bootstrap_components as dbc

#set the path so that the dataset can be read
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()
data = pd.read_csv(DATA_PATH.joinpath("dataForScatter.csv"))

#get all unique school names
schools=data["school_name"].unique()
label_school=[]
#creating a dict so that this can be used in a drop down
for l in schools:
    dict_label={"label":l,"value":l}
    label_school.append(dict_label)
#select a school, so that we always have a school selected
first_school=label_school[0]["value"]

#create layout for the page
layout=html.Div([
    #header & introduction
    html.H1("NY City school explorer - Predict the Graduation Rate", style={"textAlign":"center"}),
    html.Span("Here you see the predicted graduation rate of a school you picked. The sliders give you the opportunity "
              "to manipulate the features of the area around a school. Using this new input a prediction is generated."
              "By manipulating the features and seeing the effect, we hope you get a better understanding of the impact "
              "each feature has."
              ),

    #dropdown to select schools, using the dict from above & setting the standard value as the first school from above
    html.Div([
    dcc.Dropdown(id="school",
                 options=label_school,
                 searchable=True,
                 clearable=False,
                 value=first_school
                 ),
    ]),
    #creating all the sliders, all of them are created in the same way: minimum is zero, maximum is the maximum of
    # #features we observed in our dataset, a tooltip is explaining what the sliders can do
    #slider trees
    html.Div([
    html.Span("Number of trees", id="tipTrees"),
    dbc.Tooltip("Set the number of trees that should be assumed in the neighborhood of a school", target="tipTrees",
                placement="bottom-end"),
    dcc.Slider(
        id="trees",
        min=0,
        max=data["trees"].max(),
        step=1,
        value=10,
        marks={
            0:{"label":"0"},
            int(data["trees"].max()//2):{"label":str((data["trees"].max()//2))},
            int(data["trees"].max()):{"label":str(data["trees"].max())}},
        tooltip={"placement": "bottom", "always_visible": True}
    ),
    #slider crashes
    html.Span("Number of vehicle crashes", id="tipCrashes"),
    dbc.Tooltip("Set the number of vehicle crashes that should be assumed in the neighborhood of a school", target="tipCrashes",
                placement="bottom-end"),
    dcc.Slider(
        id="crashes",
        min=0,
        max=data["crashes"].max(),
        step=1,
        value=10,
        marks={
            0:{"label":"0"},
            int(data["crashes"].max()//2):{"label":str((data["crashes"].max()//2))},
            int(data["crashes"].max()):{"label":str(data["crashes"].max())}},
        tooltip={"placement": "bottom", "always_visible": True}
    ),
    #slider pcs
    html.Span("Number of public computers", id="tipPc"),
    dbc.Tooltip("Set the number of public computers that should be assumed in the neighborhood of a school",
                target="tipPc", placement="bottom-end"),
    dcc.Slider(
        id="pc",
        min=0,
        max=data["pc"].max(),
        step=1,
        value=10,
        marks={
            0:{"label":"0"},
            int(data["pc"].max()//2):{"label":str((data["pc"].max()//2))},
            int(data["pc"].max()):{"label":str(data["pc"].max())}},
        tooltip={"placement": "bottom", "always_visible": True}
    ),
    #slider shootings
    html.Span("Number of shootings",id="tipShootings"),
    dbc.Tooltip("Set the number of shootings that should be assumed in the neighborhood of a school", target="tipShootings",
                placement="bottom-end"),
    dcc.Slider(
        id="shootings",
        min=0,
        max=data["shootings"].max(),
        step=1,
        value=10,
        marks={
            0:{"label":"0"},
            int(data["shootings"].max()//2):{"label":str((data["shootings"].max()//2))},
            int(data["shootings"].max()):{"label":str(data["shootings"].max())}},
        tooltip={"placement": "bottom", "always_visible": True}
    ),
    #slider arrests
    html.Span("Number of arrests",id="tipArrests"),
    dbc.Tooltip("Set the number of arrests that should be assumed in the neighborhood of a school", target="tipArrests",
                placement="bottom-end"),
    dcc.Slider(
        id="arrests",
        min=0,
        max=data["arrests"].max(),
        step=1,
        value=10,
        marks={
            0:{"label":"0"},
            int(data["arrests"].max()//2):{"label":str((data["arrests"].max()//2))},
            int(data["arrests"].max()):{"label":str(data["arrests"].max())}},
        tooltip={"placement": "bottom", "always_visible": True}
    ),
    #slider after school programs
    html.Span("Number of after school programs",id="tipPrograms"),
    dbc.Tooltip("Set the number of after school programs that should be assumed in the neighborhood of a school", target="tipPrograms",
                placement="bottom-end"),
    dcc.Slider(
        id="programs",
        min=0,
        max=data["programs"].max(),
        step=1,
        value=10,
        marks={
            0:{"label":"0"},
            int(data["programs"].max()//2):{"label":str((data["programs"].max()//2))},
            int(data["programs"].max()):{"label":str(data["programs"].max())}},
        tooltip={"placement": "bottom", "always_visible": True}
    ),
    #slider bins
    html.Span("Number of Public Recycling Bins", id="tipBins"),
    dbc.Tooltip("Set the number of public recycling bin that should be assumed in the neighborhood of a school",
                target="tipBins", placement="bottom-end"),
    dcc.Slider(
        id="bins",
        min=0,
        max=data["bins"].max(),
        step=1,
        value=10,
        marks={
            0:{"label":"0"},
            int(data["bins"].max()//2):{"label":str((data["bins"].max()//2))},
            int(data["bins"].max()):{"label":str(data["bins"].max())}},
        tooltip={"placement": "bottom", "always_visible": True}
    )]),

    #showing the results of the prediction & a legend
    html.Div([
        html.Div(
        [html.Img(id="Pred", style={"width":"20%"}), # the result of our prediction
         #creating the legend
        html.Div([
        html.P("Best category", style={"background":"rgb(174,221,21)","width":"20%"}),
        html.P("Second best category",style={"background":"rgb(222,255,184)","width":"20%"}),
        html.P("Middle category",style={"background":"rgb(255,251,128)","width":"20%"}),
        html.P("Second worst category",style={"background":"rgb(255,101,51)","width":"20%"}),
        html.P("Worst category",style={"background":"rgb(239,23,46)","width":"20%"})
        ],style={ "display":"flex", "flex-direction":"row"})
        ]),
        ],style={ "display":"flex", "fley-direction":"column"}),
    #getting a text on how the output result should be understand
    html.Div(id='slider-output', style={"display":"inline-block", "width":"50%"}),


])
#creating all the callbacks to make it interactive

#set the sliders to the value of the school
@app.callback([Output(component_id="trees",component_property="value"),
               Output(component_id="crashes",component_property="value"),
               Output(component_id="pc",component_property="value"),
               Output(component_id="shootings",component_property="value"),
               Output(component_id="arrests",component_property="value"),
               Output(component_id="programs",component_property="value"),
               Output(component_id="bins",component_property="value")],
              Input(component_id= "school", component_property="value"))
def set_sliderValues(school):
    df=data[data["school_name"]==school]
    trees=df["trees"].to_list()[0]
    crashes=df["crashes"].to_list()[0]
    pc=df["pc"].to_list()[0]
    shootings=df["shootings"].to_list()[0]
    arrests=df["arrests"].to_list()[0]
    programms= df["programs"].to_list()[0]
    bins= df["bins"].to_list()[0]
    return trees,crashes,pc,shootings,arrests,programms,bins


#get the values of the sliders, either set by the user or set as a result of the values of the school
@app.callback([Output(component_id="slider-output",component_property="children"),
               Output(component_id="Pred",component_property="src")],
              [Input(component_id="trees",component_property="value"),
               Input(component_id="crashes",component_property="value"),
               Input(component_id="pc",component_property="value"),
               Input(component_id="shootings",component_property="value"),
               Input(component_id="arrests",component_property="value"),
               Input(component_id="programs",component_property="value"),
               Input(component_id="bins",component_property="value")])

def get_Prediction(trees,crashes,pc,shootings,arrests,programs,bins):
    #transforming the input in a dataframe
    dict_feat = {"trees": [trees], "crashes": [crashes], "pc": [pc], "shootings": [shootings],
                 "arrests": [arrests], "programs": [programs], "bins": [bins]}
    feat = pd.DataFrame(data=dict_feat)

    #use the dataframe to get the prediction using our model, for more information see getPrediction.py
    pred = get_pred(feat)[0]

    #get text output based on the prediction & select the right image
    if pred ==0:
        res="which is the worst category."
        filename = "zero.jpeg"
    if pred == 1:
        res="which is the second worst category."
        filename = "one.jpeg"
    if pred == 2:
        res = "which is the middle category."
        filename = "two.jpeg"
    if pred == 3:
        res= "which is the second best category."
        filename = "three.jpeg"
    if pred == 4:
        res="which is the best category."
        filename = "four.jpeg"
    fname = "/assets/" + filename

    #formatting a result string with the used features & the prediction
    res_str='We are categorizing the school graduation rate in five different categories. The best possible ' \
            'category is 4 and the worst is 0. \n' \
            'Based on your selection of {trees} trees, {crashes} crashes, {pc} pc, {shootings} shootings, ' \
            '{arrests} arrests,  {programs} programs, {bins} bins the predicted graduation rate is {pred}, {res}' \
            .format(trees=trees,crashes=crashes,pc=pc, shootings=shootings,
                                                        arrests=arrests,programs=programs,bins=bins, pred=pred, res=res)
    return res_str, fname





