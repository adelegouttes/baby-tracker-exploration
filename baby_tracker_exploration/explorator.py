import os

import numpy as np
import pandas as pd

CURRENT_FOLDER = os.path.abspath(os.path.dirname(__file__))
DATA_PATH = os.path.join(CURRENT_FOLDER, "data/BabyRecords.csv")


def compute_daily_statistics_feeding(feeding_df: pd.DataFrame) -> pd.DataFrame:
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

    result.columns = rename_summary_columns(result)

    return result


def compute_summary_statistics_diapering(df: pd.DataFrame) -> pd.DataFrame:
    cost_disposable_diapers = 0.14
    initial_investment = 100
    total_diapers = df["IsNewDiaper_sum"].sum()
    savings_diapers = cost_disposable_diapers * total_diapers
    avg_nb_diapers_per_day = df["IsNewDiaper_sum"].mean()
    summary_data = {
        "Total number of diapers (count)": total_diapers,
        "Savings vs buying disposable diapers (euros)": savings_diapers,
        "Savings after initial investment (euros)": savings_diapers - initial_investment,
        "Average number of diapers per day": avg_nb_diapers_per_day
    }
    return pd.DataFrame(data=summary_data.values(), columns=["Value"], index=summary_data.keys())


def compute_daily_statistics_diapering(df):
    result = df.assign(
        IsNewDiaper=1,
    )
    result = result.groupby(["StartDateDay"]).agg(
        {"IsNewDiaper": [np.sum]}
    )
    result.columns = rename_summary_columns(result)
    return result


def rename_summary_columns(df):
    return ["_".join(col).strip() for col in df.columns.values]


def compute_summary_statistics_feeding(df):
    nb_good_nights = df.loc[df["TimeFromPreviousFeed_max"] > 5.]["TimeFromPreviousFeed_max"].count()
    share_of_good_nights = nb_good_nights / len(df)
    avg_max_sleeping_time = df["TimeFromPreviousFeed_max"].mean()
    avg_nb_feeds_per_day = df["IsNewFeed_sum"].mean()
    avg_time_bet_feeds = df["TimeFromPreviousFeed_mean"].mean()

    data = {
        "Number of good sleeping nights (count)": [nb_good_nights],
        "Share of good sleeping nights (%)": [share_of_good_nights],
        "Average time of the longest sleep (hours)": [avg_max_sleeping_time],
        "Average number of feeds per day (count)": [avg_nb_feeds_per_day],
        "Average time between feeds (hours)": [avg_time_bet_feeds],
    }
    results = pd.DataFrame(data=data.values(), columns=["Value"], index=data.keys())

    return results
