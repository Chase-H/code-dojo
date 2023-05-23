import fire
import pandas as pd
import pprint

def load_data():
    return pd.read_csv("close_encounters.csv")


class App:
    def shuffle_descriptions(self, sample_num):
        df = load_data()
        print("Enjoy some random descriptions:")
        for d in df["description"].sample(sample_num):
            pprint.pprint(d)
            print("\n")

if __name__ == "__main__":
    fire.Fire(App)