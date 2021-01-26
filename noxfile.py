import nox


# Sessions that nox will run by default, if no session is specified
nox.options.sessions = "lint", "mypy", "tests"


# Useful option:
# `nox -r` reuses the existing venvs, instead of building them from scratch
# `nox --list`
# `nox --sessions lint `


@nox.session(python=["3.7"])
def tests(session):
    args = session.posargs or ["--cov"]  # Example: --cov to use test coverage
    session.run("poetry", "install", external=True)
    session.run("pytest", *args)


locations = "baby_tracker_exploration", "tests", "noxfile.py"


@nox.session(python=["3.7"])
def lint(session):
    args = session.posargs or locations
    session.install("flake8", "flake8-black", "flake8-import-order")
    session.run("flake8", *args)


@nox.session(python="3.7")
def black(session):
    args = session.posargs or locations
    session.install("black")
    session.run("black", *args)


@nox.session(python=["3.7"])
def mypy(session):
    args = session.posargs or locations
    session.install("mypy")
    session.run("mypy", *args)
