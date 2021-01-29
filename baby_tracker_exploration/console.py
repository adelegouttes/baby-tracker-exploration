import click

from baby_tracker_exploration.explorator import run_exploration


@click.command()
@click.option("--min-date", default=None, type=str, help="Format: YYYY-MM-DD")
@click.option("--max-date", default=None, type=str, help="Format: YYYY-MM-DD")
def main(min_date, max_date):
    run_exploration(min_date=min_date, max_date=max_date)
