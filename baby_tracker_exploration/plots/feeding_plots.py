import pandas as pd
from plotly import express as px, graph_objects as go


def plot_avg_time_bet_feeds(plot_df):
    """Average time between Feeds"""
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
    return fig_3


def plot_nb_feeds_per_day(plot_df):
    """Number of feeds per day"""
    fig_2 = go.Figure()
    fig_2.add_trace(
        go.Bar(x=plot_df.index, y=plot_df["IsNewFeed_sum"], marker_color="brown")
    )
    fig_2.update_layout(
        title="Number of Feed per Day",
        xaxis_title="Day",
        yaxis_title="Count",
    )
    return fig_2


def plot_max_time_bet_feeds(plot_df):
    """Max time between Feeds"""
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
    return fig_1


def plot_daily_statistics_feeding(plot_df: pd.DataFrame):

    fig_1 = plot_max_time_bet_feeds(plot_df)

    fig_2 = plot_nb_feeds_per_day(plot_df)

    fig_3 = plot_avg_time_bet_feeds(plot_df)

    return fig_1, fig_2, fig_3
