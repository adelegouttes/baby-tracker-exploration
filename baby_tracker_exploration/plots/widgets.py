from ipywidgets import Layout, widgets
import pandas as pd


def generate_date_widget(df: pd.DataFrame) -> widgets.SelectionRangeSlider:
    min_date, max_date = df.index.min(), df.index.max()
    date_widget = widgets.SelectionRangeSlider(
        options=["{:%Y/%m/%d}".format(d) for d in pd.date_range(min_date, max_date)],
        index=(0, 2),
        description="Date Range:",
        disabled=False,
        style={"description_width": "initial"},
        layout=Layout(width="600px"),
    )
    return date_widget
