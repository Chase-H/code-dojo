import typer
import pandas as pd
from rich import print
from rich.table import Table

app = typer.Typer()

def load_data():
    return pd.read_csv("close_encounters.csv")

def combine_city_state(row):
    city = row['city']
    state = row['state']
    
    if city and state:
        return f"{city}, {state}"
    elif city:
        return city
    elif state:
        return state
    else:
        return None

def get_top_cities(df, shape: str, top_n: int):
    filtered_df = df[df['type'] == shape].copy()
    filtered_df['city_state'] = filtered_df.apply(combine_city_state, axis=1)
    filtered_df['city_state'] = filtered_df.apply(combine_city_state, axis=1)
    city_counts = filtered_df["city_state"].value_counts()
    return city_counts.nlargest(top_n)

@app.command()
def top_sightings(shape: str = "circle", top_n: int = 10, debug: bool = False):
    if debug:
        typer.echo("Debug mode is on")

    df = load_data()
    
    if debug:
        typer.echo(f"Filtering by shape: {shape}")

    top_cities = get_top_cities(df, shape, top_n)

    if debug:
        typer.echo("Displaying results:")
    
    for index, (city, count) in enumerate(top_cities.items(), start=1):
        print(f"{index}. {city}, state: {count} sightings")
        
        
@app.command()
def top_sightings_with_style(shape: str = "circle", top_n: int = 10, debug: bool = False):
    if debug:
        typer.echo("Debug mode is on")

    df = load_data()

    if debug:
        typer.echo(f"Filtering by shape: {shape}")

    top_cities = get_top_cities(df, shape, top_n)

    if debug:
        typer.echo("Displaying results:")

    table = Table(title=f"Top {top_n} Cities with {shape.capitalize()} UFO Sightings")
    table.add_column("Rank", justify="right")
    table.add_column("City")
    table.add_column("Sightings", justify="right")

    for index, (city, count) in enumerate(top_cities.items(), start=1):
        table.add_row(str(index), city, str(count))

    print(table)


if __name__ == "__main__":
    app()