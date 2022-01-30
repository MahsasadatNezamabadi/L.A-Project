import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import numpy as np

model=pickle.load(open("final_model.sav","rb"))
meanStd=pd.read_csv("datasets/meanStd.csv",index_col=0)

def get_pred(features, model=model,meanStd=meanStd):
    for col in features.columns:
        std=meanStd.at["std",col]
        mean=meanStd.at["mean",col]
        features[col]=((features[col]-mean)/std)
    pred=model.predict(features)


    return pred






