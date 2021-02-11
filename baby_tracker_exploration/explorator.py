from datetime import timedelta
import os

import dateparser
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


CURRENT_FOLDER = os.path.abspath(os.path.dirname(__file__))
DATA_PATH = os.path.join(CURRENT_FOLDER, "data/BabyRecords.csv")


def get_baby_tracker_data(data_path: str = DATA_PATH) -> pd.DataFrame:
    result = pd.read_csv(
        data_path, parse_dates=["StartDate", "FinishDate"], date_parser=dateparser.parse
    )
    expected_columns = ["RecordCategory", "StartDate", "FinishDate"]
    if not all(e in result.columns for e in expected_columns):
        raise ValueError(
            "Your file contains the following columns: {current_col}"
            "The CSV must contain at least the following columns: {expected_col} \n"
            "Check the file example: baby_tracker_exploration/data/ExampleFile.csv"
            "".format(current_col=result.columns, expected_col=expected_columns)
        )
    return result


def get_feeding_data(df: pd.DataFrame) -> pd.DataFrame:
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


def show_daily_statistics(plot_df: pd.DataFrame):

    # -------- Max time between Feeds
    fig_1 = px.line(
        plot_df,
        x=plot_df.index,
        y="TimeFromPreviousFeed_max",
        title="Max Sleeping Time at Night (Maximum Time between Feeds per Day)",
        labels={
            "TimeFromPreviousFeed_max": "Max Sleeping Time at Night (hour)",
            "StartDateDay": "Day",
        },
    )

    # -------- Number of feeds per day
    fig_2 = go.Figure()
    fig_2.add_trace(
        go.Bar(x=plot_df.index, y=plot_df["IsNewFeed_sum"], marker_color="brown")
    )
    fig_2.update_layout(
        title="Number of Feed per Day",
        xaxis_title="Day",
        yaxis_title="Count",
    )

    # -------- Average time between Feeds
    fig_3 = go.Figure()
    fig_3.add_trace(
        go.Scatter(
            x=plot_df.index,
            y=plot_df["TimeFromPreviousFeed_mean"],
            mode="lines",
            line=dict(color="green"),
        )
    )
    fig_3.update_layout(
        title="Average Time between Feeds per Day",
        xaxis_title="Day",
        yaxis_title="Hours",
    )

    return fig_1, fig_2, fig_3
