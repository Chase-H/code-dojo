import click
import pandas as pd


def load_data():
    return pd.read_csv("close_encounters.csv")


@click.group()
def cli():
    pass

@click.group()
def count():
    pass

cli.add_command(count)

@count.command()
@click.argument("shape")
def shape(shape):
    df = load_data()
    count_shape = df[df["type"] == shape].shape[0]
    click.echo(f"Number of {shape} sightings: {count_shape}")

@count.command()
@click.argument("date")
def before(date):
    df = load_data()
    df["date"] = pd.to_datetime(df["date"])
    date = pd.to_datetime(date)
    count_before = df[df["date"] < date].shape[0]
    click.echo(f"Number of encounters before {date.strftime('%m/%d/%Y')}: {count_before}")

@count.command()
@click.argument("date")
def after(date):
    df = load_data()
    df["date"] = pd.to_datetime(df["date"])
    date = pd.to_datetime(date)
    count_after = df[df["date"] > date].shape[0]
    click.echo(f"Number of encounters after {date.strftime('%m/%d/%Y')}: {count_after}")

@click.group()
def details():
    pass

cli.add_command(details)

@details.command()
@click.argument("column_name")
def column(column_name):
    df = load_data()
    distinct_values = df[column_name].unique()
    click.echo(f"Distinct values for {column_name}:")
    for value in distinct_values:
        click.echo(value)
    
if __name__ == "__main__":
    cli()