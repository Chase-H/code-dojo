import pandas as pd
import ast
import re
import concurrent.futures
import collections
import os
import time
import pprint


df = pd.read_csv("Philosophers-dataset.csv")

new_df = df[["Born", "Birth place", "Died", "Subjects Of Study", "Philosophers"]]
new_df = new_df.dropna()
new_df = new_df[new_df["Born"].str.contains("BCE") == False] # Don't want to deal with BCE dates; sorry Socrates


def get_country(places):
    if not places:
        return None
    else:
        return places[-1]
    
new_df["Birth Country"] = new_df['Birth place'].apply(lambda x: ast.literal_eval(x)).apply(get_country)
# This is ugly, but I got a bit lazy; will endeavor to beautify later
new_df["Born"] = new_df["Born"].apply(lambda x: x.split(", ")[-1]).apply(lambda x: x.split(". ")[-1]).apply(lambda x: x.split(" ")[-1]).apply(lambda x: x.replace("?", "")).apply(lambda x: int(x))
new_df["Died"] = new_df["Died"].apply(lambda x: x.split(", ")[-1]).apply(lambda x: re.sub("[\(\[].*?[\)\]]", "", x)).apply(lambda x: x.split(". ")[-1]).apply(lambda x: x.split(" ")[-1] if x.split(" ")[-1] != "" else x.split(" ")[0]).apply(lambda x: x.replace(")", "")).apply(lambda x: x.replace("?", "")).apply(lambda x: int(x))
del new_df["Birth place"]
new_df.columns = ["_".join(i.lower().split(" ")) for i in new_df.columns]
new_df = new_df.dropna()
new_df = new_df.rename(columns={"philosophers": "name"})

# We'll need this for the reduce section later 
all_subjects = list(set([a for b in new_df["subjects_of_study"].apply(lambda x: x.split(", ")).tolist() for a in b]))
all_countries = list(set([x for x in new_df["birth_country"].tolist()]))
Philosopher = collections.namedtuple("Philosopher", [
    "born",
    "died",
    "subjects_of_study",
    "name",
    "birth_country"
])

philosophers = [Philosopher(*row) for row in new_df.itertuples(index=False, name=None)]

def transform(x):
    print(f"Process ID {os.getpid()} is processing philosopher: {x.name}")
    time.sleep(.01)
    return {"name": x.name, "age": x.died - x.born}


if __name__=="__main__":
    with concurrent.futures.ProcessPoolExecutor() as executor:
        result = executor.map(transform, philosophers)
    pprint.pprint(tuple(result))