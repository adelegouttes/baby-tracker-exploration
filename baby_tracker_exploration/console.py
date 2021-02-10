import os

import click

ABS_PATH = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), "explorator.ipynb"
)

@click.command()
def main():
    os.system("ipython kernel install --user --name=baby-tracker-exploration")
    os.system("jupyter-notebook {path} --kernel baby-tracker-exploration ".format(path=ABS_PATH))
