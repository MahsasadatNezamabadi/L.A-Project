from dash import dcc
from dash import html

#this is the first page & default page one would see, ideally there would be more about the project
layout=html.Div([
    html.Span("This application will give you an overview about the graduation rate in New York City. It will also help "
              "you understand what influence the close environment has on the graduation rate."
              "In the first part (Discover the Data) you will be able to have a look at the different aspects of the "
              "environment and how they may influence the average graduation rate."
              "The second part (Predict the graduation rate) will present you a machine learning model, which predicts"
              "the graduation rate of a school. You are also able to change the input of the features to get a better "
              "understanding of how different features influence the graduation rate."
              ),
])