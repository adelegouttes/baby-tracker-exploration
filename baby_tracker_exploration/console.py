import os

import click
import pandas as pd


DATA_PATH = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), "data/BabyRecords.csv"
)


def get_data(data_path=DATA_PATH):
    df = pd.read_csv(data_path)
    feeding_df = df.loc[df.RecordCategory == "Feeding"]
    print(feeding_df.head())


@click.command()
def main():
    return get_data()
