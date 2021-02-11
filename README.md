# baby-tracker-exploration

With this repository, you can run data analyses on a collection of data about 
breast feeding. The data was collected using a mobile app, from which it is possible to export a csv file. 

This repository is also a good opportunity to use the following tools:
- managing your repository: poetry, nox, black, flake8, pytest (read this [blog post](https://medium.com/@cjolowicz/hypermodern-python-d44485d9d769) )
- explore your dataset: pandas
- plot your graphs with a nice UI: jupyter, plotly, ipywidgets (inspiration from this [post](https://nonvisual.github.io/2020/11/22/budget-optimization-intro/))

## How to use
* [Install poetry](https://python-poetry.org/docs/#installation) on your machine and clone this repository. Ensure you have python 3.7 installed on your machine. 
* Go inside the cloned repository and initialize poetry: 
```
cd baby-tracker-exploration
poetry init
```
* Start the jupyter-notebook `explorator.ipynb` running the following command:
```
poetry run explore
```