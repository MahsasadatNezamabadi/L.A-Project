import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import numpy as np

model=pickle.load(open("../final_model.sav","rb"))
meanStd=pd.read_csv("../datasets/meanStd.csv",index_col=0)
print(meanStd)
def get_pred(features, model=model,meanStd=meanStd):
    for col in features.columns:
        std=meanStd.at["std",col]
        mean=meanStd.at["mean",col]
        features[col]=((features[col]-mean)/std)
    pred=model.predict(features)


    return pred

test=np.array([[15],[4],[3],[2],[89],[10],[2]])
test= {"trees":[15], "crashes":[4], "pc":[3], "shootings":[2], "arrests":[89], "programs":[10],
       "bins":[2]}
testDf=pd.DataFrame(data=test)




