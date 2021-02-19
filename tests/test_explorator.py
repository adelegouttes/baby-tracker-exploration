import os

import pandas as pd
import pytest

from baby_tracker_exploration.data_pipeline.data_preparation import (
    get_baby_tracker_data,
    prepare_diapering_data,
    prepare_feeding_data,
)
from baby_tracker_exploration.explorator import (
    compute_daily_statistics_diapering,
    compute_daily_statistics_feeding,
    compute_summary_statistics_diapering,
    compute_summary_statistics_feeding,
    CURRENT_FOLDER,
)
from baby_tracker_exploration.plots import plot_daily_statistics_feeding


@pytest.fixture()
def wrong_df():
    return pd.DataFrame({"var_1": [1, 2, 3]})


@pytest.fixture()
def example_file_path():
    return os.path.join(CURRENT_FOLDER, "data/ExampleFile.csv")


def test_get_baby_tracker_data(tmpdir, wrong_df, example_file_path):

    wrong_csv_path = tmpdir.mkdir("sub").join("wrong.csv")
    wrong_df.to_csv(wrong_csv_path)
    with pytest.raises(ValueError):
        get_baby_tracker_data(wrong_csv_path)

    get_baby_tracker_data(example_file_path)


@pytest.fixture()
def baby_tracker_df(example_file_path):
    return get_baby_tracker_data(example_file_path)


def test_feeding_exploration(baby_tracker_df):
    feeding_df = prepare_feeding_data(baby_tracker_df)
    daily_statistics = compute_daily_statistics_feeding(feeding_df)
    compute_summary_statistics_feeding(daily_statistics)
    plot_daily_statistics_feeding(daily_statistics)


def test_diapering_exploration(baby_tracker_df):
    diapering_df = prepare_diapering_data(baby_tracker_df)
    daily_statistics = compute_daily_statistics_diapering(diapering_df)
    compute_summary_statistics_diapering(daily_statistics)
