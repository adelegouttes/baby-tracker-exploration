from datetime import datetime, timedelta

import dateparser
import pandas as pd

from baby_tracker_exploration.explorator import DATA_PATH


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

    start_date_day = result["StartDate"].apply(lambda d: d.date())

    return result.assign(StartDateDay=start_date_day,)


def prepare_feeding_data(df: pd.DataFrame) -> pd.DataFrame:
    feeding_df = df.loc[df["RecordCategory"] == "Feeding"].sort_values(by="StartDate")

    start_previous_feed = feeding_df["StartDate"].shift(1)
    time_from_previous_feed = feeding_df["StartDate"] - start_previous_feed
    time_limit = timedelta(minutes=30)

    feeding_df = feeding_df.assign(
        IsNewFeed=time_from_previous_feed > time_limit,
    )

    feeding_df = feeding_df.loc[feeding_df["IsNewFeed"]]

    feed_duration = feeding_df["FinishDate"] - feeding_df["StartDate"]
    start_previous_feed = feeding_df["StartDate"].shift(1)
    time_from_previous_feed = feeding_df["StartDate"] - start_previous_feed

    return feeding_df.assign(
        FeedDuration=feed_duration,
        StartPreviousFeed=start_previous_feed,
        TimeFromPreviousFeed=time_from_previous_feed,
    )


def prepare_diapering_data(df, min_date=datetime(2021, 1, 1)):
    result = df.loc[
        (df["RecordCategory"] == "Diapering")
        & (df["StartDate"] > min_date)
    ]
    result = result.set_index("StartDate")
    return result
