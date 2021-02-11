import os

import pandas as pd
import pytest

from baby_tracker_exploration.explorator import (
    compute_daily_statistics,
    CURRENT_FOLDER,
    get_baby_tracker_data,
    get_feeding_data,
    prepare_feeding_data,
    show_daily_statistics,
)


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


def test_exploration_goes_through(example_file_path):
    main_df = get_baby_tracker_data(example_file_path)
    feeding_df = get_feeding_data(main_df)
    feeding_df = prepare_feeding_data(feeding_df)
    daily_statistics = compute_daily_statistics(feeding_df)
    show_daily_statistics(daily_statistics)
