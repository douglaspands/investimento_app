import subprocess


def shell(command: str | list[str]):
    print(f"$ {command if isinstance(command, str) else ' '.join(command)}")
    return subprocess.run(command, check=True, shell=True)


def test():
    shell(
        "pytest --cov=app --cov-report=term-missing --cov-report=xml:coverage.xml --cov-report=html"
    )


def format():
    shell("ruff check --select I --fix")
    shell("ruff format")


def check():
    shell("ruff check .")


def build():
    hidden_import = ["aiosqlite", "shellingham.posix", "logging.config", "tzdata"]
    shell(
        " ".join(
            [
                "pyinstaller",
                "--python-option",
                '"PYTHONDONTWRITEBYTECODE=1"',
                "--name",
                "trader",
                *(" ".join([f"--hiddenimport {hi}" for hi in hidden_import])).split(
                    " "
                ),
                "--runtime-hook",
                "./script/hook.py",
                "--add-data",
                "./pyproject.toml:./",
                "--add-data",
                "./alembic.ini:./",
                "--add-data",
                "./migration:./migration",
                "--console",
                "--noconfirm",
                "./main.py",
            ]
        )
    )


def pycache_remove():
    for folder in ["app", "tests", "migration"]:
        shell(f"cd {folder} && find . -type d -name '__pycache__' | xargs rm -rf")
