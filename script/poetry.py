import platform
import subprocess

folder_sep = "/" if platform.system() in ("Linux",) else "\\"


def shell(command: str | list[str]):
    return subprocess.run(command, check=True, shell=True)


def test():
    shell("pytest --cov=app --cov-report=term-missing --cov-report=html")


def format():
    shell("ruff check --select I --fix")
    shell("ruff format")


def check():
    shell("ruff check .")


def build():
    shell(
        " ".join(
            [
                "pyinstaller",
                "--python-option",
                '"PYTHONDONTWRITEBYTECODE=1"',
                "--name",
                "trader",
                "--hiddenimport",
                "aiosqlite",
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
