from datetime import timedelta
import os

import click
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

DATA_PATH = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), "data/BabyRecords.csv"
)


def get_feeding_data(data_path: str = DATA_PATH) -> pd.DataFrame:
    df = pd.read_csv(data_path, parse_dates=["StartDate", "FinishDate"])
    feeding_df = df.loc[df["RecordCategory"] == "Feeding"].sort_values(by="StartDate")

    start_previous_feed = feeding_df["StartDate"].shift(1)
    time_from_previous_feed = feeding_df["StartDate"] - start_previous_feed
    time_limit = timedelta(minutes=30)

    return feeding_df.assign(
        IsNewFeed=time_from_previous_feed > time_limit,
        TimeFromPreviousBreast=time_from_previous_feed,
    )


def prepare_feeding_data(feeding_df: pd.DataFrame) -> pd.DataFrame:
    df = feeding_df.loc[feeding_df["IsNewFeed"]]

    start_date_day = df["StartDate"].apply(lambda d: d.date())
    feed_duration = df["FinishDate"] - df["StartDate"]
    start_previous_feed = df["StartDate"].shift(1)
    time_from_previous_feed = df["StartDate"] - start_previous_feed

    return df.assign(
        StartDateDay=start_date_day,
        FeedDuration=feed_duration,
        StartPreviousFeed=start_previous_feed,
        TimeFromPreviousFeed=time_from_previous_feed,
    )


def compute_daily_statistics(feeding_df: pd.DataFrame) -> pd.DataFrame:
    mean_agg = pd.NamedAgg(
        column="mean", aggfunc=lambda d: pd.Series.mean(d) / pd.Timedelta(hours=1)
    )
    max_agg = pd.NamedAgg(
        column="max", aggfunc=lambda d: np.max(d) / pd.Timedelta(hours=1)
    )
    sum_agg = pd.NamedAgg(
        column="sum", aggfunc=lambda d: np.sum(d) / pd.Timedelta(hours=1)
    )
    result = feeding_df.groupby(feeding_df["StartDateDay"]).agg(
        {
            "TimeFromPreviousFeed": [mean_agg, max_agg],
            "IsNewFeed": [np.sum],
            "FeedDuration": [sum_agg, mean_agg, max_agg],
        }
    )

    result.columns = ["_".join(col).strip() for col in result.columns.values]

    return result


def show_daily_statistics(feeding_df: pd.DataFrame):
    daily_statistics = compute_daily_statistics(feeding_df)

    min_date, max_date = daily_statistics.index.min(), daily_statistics.index.max()

    first_sunday = min_date + timedelta(days=(min_date.day - min_date.weekday() + 7) % 7)
    last_sunday = max_date - timedelta(days=(max_date.day - max_date.weekday() + 7) % 7)
    sunday_dates = pd.date_range(start=first_sunday, end=last_sunday, periods=7)

    # -------- Max time between Feeds
    plt.plot()
    daily_statistics["TimeFromPreviousFeed_max"].plot(
        style=".-",
        figsize=(20, 5),
        title="Maximum Time between Feeds",
        ylabel="Hours"
    )
    plt.vlines(sunday_dates, ymin=0, ymax=12, colors="grey", linestyles="dotted")
    plt.hlines(list(range(0, 12, 2)), xmin=min_date, xmax=max_date, colors="grey", linestyles="dotted")
    plt.show()

    # -------- Number of feeds per day
    plt.plot()
    daily_statistics["IsNewFeed_sum"].plot(
        style=".-",
        color="lightgreen",
        figsize=(20, 5),
        title="Number of feed per day",
        ylabel="Count",
        kind="bar"
    )
    plt.vlines(sunday_dates, ymin=0, ymax=daily_statistics["IsNewFeed_sum"].max(), colors="grey", linestyles="dotted")
    plt.hlines([5, 10], xmin=min_date, xmax=max_date, colors="grey", linestyles="dotted")
    plt.show()

    # -------- Average time between Feeds
    plt.plot()
    daily_statistics["TimeFromPreviousFeed_mean"].plot(
        style=".-",
        color="orange",
        figsize=(20, 5),
        title="Average Time between Feeds",
        ylabel="Hours"
    )
    plt.vlines(sunday_dates, ymin=0, ymax=5, colors="grey", linestyles="dotted")
    plt.hlines(list(range(5)), xmin=min_date, xmax=max_date, colors="grey", linestyles="dotted")
    plt.show()


def run_analysis():
    feeding_df = get_feeding_data()
    feeding_df = prepare_feeding_data(feeding_df)
    show_daily_statistics(feeding_df)

@click.command()
def main():
    run_analysis()
