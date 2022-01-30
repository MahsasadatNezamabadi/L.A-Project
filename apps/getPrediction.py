import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

model=pickle.load(open("../final_model.sav","rb"))

def get_pred(features):
    pred=model.predict(features)

    return pred

print(get_pred([15,4,3,2,89,10,2]))
