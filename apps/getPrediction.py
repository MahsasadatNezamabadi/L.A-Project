import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
#method to load the created machine learning model & get the prediction

#loadingt the model
model=pickle.load(open("final_model.sav","rb"))
#need the mean Std in our dataset for each feature, because we built our model on standardized data
#so we need to standardize the input in our model
meanStd=pd.read_csv("datasets/meanStd.csv",index_col=0)

def get_pred(features, model=model,meanStd=meanStd):
    #features is a dataframe, containing the number of features on which we want to use for our prediction
    #first step is to standardize our input
    for col in features.columns:
        std=meanStd.at["std",col]
        mean=meanStd.at["mean",col]
        features[col]=((features[col]-mean)/std)
    #getting the prediction from our model
    pred=model.predict(features)
    return pred






