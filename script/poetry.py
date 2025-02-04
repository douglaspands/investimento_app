import subprocess


def shell(command):
    return subprocess.run(command, check=True, shell=True)


def test():
    shell("pytest --cov=app --cov-report=term-missing")


def format():
    shell("ruff format .")


def check():
    shell("ruff check .")
