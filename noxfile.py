import nox

# Useful option: -r reuses the existing virtualenvs, instead of building them from scratch

@nox.session
def tests(session):
    args = session.posargs or ["--cov"] # Example: --cov to use test coverage
    session.run("poetry", "install", external=True)
    session.run('pytest', *args)

