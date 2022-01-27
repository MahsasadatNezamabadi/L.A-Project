import pandas as pd
from sodapy import Socrata
from datetime import datetime
import pickle
from geopy import distance
import numpy as np
import time
from sklearn.metrics.pairwise import haversine_distances
from math import radians

start = time.time()

dict_dfs = {}

dict_dfs = {"grad": ["nb39-jx2v"], "trees": ["uvpi-gqnh"], "crashes": ["h9gi-nx95"], "pc": ["cuzb-dmcd"],
            "shootings": ["833y-fsy8"], "arrests": ["8h9b-rp9u"], "programs": ["mbd7-jfnc"], "bins": ["sxx4-xhzg"]}
for key in dict_dfs:
    x = dict_dfs[key][0]
    dict_dfs[key] = {"key": x, "last_updated": 0, "data": ""}





get_data(dict_dfs)
print("since start", (time.time() - start) / 60)

def get_avgGradRate(df_school, df_scatter):
    df=df_school
    df1=df_scatter
    df["total_grads_of_cohort"]=df["total_grads_of_cohort"].apply(float)
    x=df.groupby(["dbn"]).mean()
    x=x.reset_index()
    x=x.rename(columns={"total_grads_of_cohort":"avg_perc Grads"})
    x=x[["dbn","avg_perc Grads"]]
    df1=df1.merge(x, on= "dbn", how="left")
    return df1

def clean_school(df_grad):
    df=df_grad
    df= df[(df["demographic_variable"]=="All Students")&(df["demographic_category"]=="All Students")]
    print(df.columns)
    df=df[["dbn","cohort_year","cohort","total_grads_of_cohort"]]
    df=df[df.total_grads_of_cohort.notnull()]
    return df


def get_dataframes(data_dict):
    data_url = "https://data.cityofnewyork.us/resource/"
    limit = ".json?$limit=1000000000&$$app_token=HnDwBjZUCabVQojpbl6aIDrDI"
    for key in data_dict:
        print(key)
        if data_dict[key]["data"] != "":
            continue
        if key in ["addresses", "scatter"]:
            continue

        t1 = time.time()

        if key == "grad":

            url = data_url + data_dict[key]["key"] + limit
            print(url)
            df = pd.read_json(url)

        else:
            time.sleep(60)
            url = data_url + data_dict[key]["key"] + limit
            df = pd.read_json(url)
            if "lat" in df.columns:
                df = df.rename(columns={"lat": "latitude", "lon": "longitude"})
            df = df[["latitude", "longitude"]]

            df = df[df.latitude.notna()]
            df = df[df.longitude.notna()]
            df["latitude"] = df["latitude"].apply(float)
            df["longitude"] = df["longitude"].apply(float)
            df["location"] = list(zip(df["latitude"].to_list(), df["longitude"].to_list()))
        end = time.time()
        print(key, ((end - t1) / 60))

        data_dict[key]["df"] = df
        print(key + " done")
    df = pd.read_csv("datasets/2016_DOE_High_School_Directory-2.csv")
    # df["location"]=list(zip(df["Latitude"].to_list(),df["Longitude"].to_list()))
    df = df.rename(columns={"Latitude": "latitude", "Longitude": "longitude"})
    df = df[["dbn", "school_name", "borough", "latitude", "longitude"]]
    df["latitude"] = df["latitude"].apply(float)
    df["longitude"] = df["longitude"].apply(float)
    df["location"] = list(zip(df["latitude"].to_list(), df["longitude"].to_list()))
    data_dict["grad"]["df"] = clean_school(dict_dfs["grad"]["df"])
    df = get_avgGradRate(data_dict["grad"]["df"], df)
    # df=df.drop(columns=[""])
    x = df[["dbn", "latitude", "longitude", "location"]]
    data_dict["grad"]["df"] = data_dict["grad"]["df"].merge(x, on="dbn", how="left")
    data_dict["scatter"] = {"df": df}


get_dataframes(dict_dfs)

with open('datasets/dictdfs.pickle', 'wb') as handle:
    pickle.dump(dict_dfs, handle, protocol=pickle.HIGHEST_PROTOCOL)

print("since start", (time.time() - start) / 60)

get_dataframes(dict_dfs)

with open('datasets/dictdfs.pickle', 'wb') as handle:
    pickle.dump(dict_dfs, handle, protocol=pickle.HIGHEST_PROTOCOL)

print("since start", (time.time() - start) / 60)


def get_radLocList(df):
    df["latitude_rad"] = df["latitude"]
    df["longitude_rad"] = df["longitude"]
    df["latitude_rad"] = df["latitude_rad"].apply(lambda x: radians(x))
    df["longitude_rad"] = df["longitude_rad"].apply(lambda x: radians(x))
    l = list(zip(df["latitude_rad"].to_list(), df["longitude_rad"].to_list()))
    return l


def getFeat(l1, l2):
    res = haversine_distances(l1, l2)
    res = res * 6371000 / 1000
    res1 = res < 0.5
    feat = np.sum(res1, axis=1)
    return feat


def allFeat(data_dict):
    t1 = time.time()
    df_scatter = data_dict["scatter"]["df"]
    lScatter = get_radLocList(df_scatter)
    for key in data_dict:
        t2 = time.time()
        if key == "grad":
            continue
        if key == "scatter":
            continue
        l_feat = get_radLocList(data_dict[key]["df"])
        feat = getFeat(lScatter, l_feat)
        df_scatter[key] = feat
        print(key, " done ", (time.time() - t2) / 60)
    df_scatter.drop(columns=["latitude_rad", "longitude_rad", "location_rad"])
    data_dict["scatter"]["df"] = df_scatter
    print("all done", (time.time() - t1) / 60)
    return df_scatter


allFeat(dict_dfs)
print("since start", (time.time() - start) / 60)

x=dict_dfs["scatter"]["df"]
x.to_csv("datasets/dataForScatter.csv")

df_scatter=x

def featuresForSchools(df_scatter, df_grad):
    df= df_grad.merge(df_scatter, on="dbn",how="left")
    df= df.drop(columns=["Unnamed: 0"])
    return df

x=featuresForSchools(df_scatter,dict_dfs["grad"]["df"])

def normalize_df(df, columns):
    for col in columns:
        df[col]=((df[col]-df[col].mean())/df[col].std())
    return df

x_norm=normalize_df(x,["trees","crashes", "pc", "shootings", "arrests","programs","bins"])
x_norm.to_csv("datasets/dataForML.csv")

end2=time.time()

print("/n/n",(end2-start)/59.992)