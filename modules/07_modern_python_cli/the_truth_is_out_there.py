import argparse
import pandas as pd

def load_data():
    return pd.read_csv("close_encounters.csv")

def city_with_most_encounters(args):
    state = args.state.lower()
    df = load_data()
    df["state"] = df["state"].str.lower()
    filtered_df = df[df["state"] == state]
    city_counts = filtered_df["city"].str.lower().value_counts()
    top_city = city_counts.idxmax()
    print(f"The city with the most UFO encounters in {state.upper()} is: {top_city.capitalize()}")

parser = argparse.ArgumentParser()
parser.add_argument("state", help="State abbreviation to find the city with the most UFO encounters")
parser.set_defaults(func=city_with_most_encounters)

args = parser.parse_args()
args.func(args)