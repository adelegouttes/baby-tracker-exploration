import os

import click


@click.command()
def main():
    os.system("ipython kernel install --user --name=baby-tracker-exploration")
    os.system("jupyter-notebook . --kernel baby-tracker-exploration ")
