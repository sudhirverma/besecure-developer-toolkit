"""This module provides the Be-Secure Developer Toolkit CLI."""
# src/cli.py
import os
import json
from typing import Optional
from typing import List
from rich import print
import typer
from besecure_developer_toolkit import __app_name__, __version__
from besecure_developer_toolkit.src.create_ossp_master import OSSPMaster
from besecure_developer_toolkit.src.create_version_data import Version
from besecure_developer_toolkit.src.generate_report import Report
import ssl
ssl._create_default_https_context = ssl._create_stdlib_context

def write_env_vars_file():
    """Creates an env var file
    """
    user_home = os.path.expanduser('~')
    vars_dir_path = f"{user_home}/.bes-dev-kit"
    vars_file_path = f"{vars_dir_path}/bes-dev-kit.json"
    env_vars = {
        "GITHUB_ORG": "Be-Secure",
        "OSSPOI_DIR": "",
        "ASSESSMENT_DIR": "",
        "GITHUB_AUTH_TOKEN": ""
    }
    if os.path.exists(vars_file_path) and os.stat(vars_file_path).st_size > 0:
        return
    os.makedirs(vars_dir_path, exist_ok=True)
    print("[bold red]Alert! [green]Creating environment variables file")
    with open(vars_file_path, 'w', encoding="utf-8") as file_pointer:
        file_pointer.write(json.dumps(env_vars, indent=4))


def prompt_user(key, value):
    """Prompts user if any env var is empty

    Args:
        key (_type_): env var key
        value (_type_): env var value

    Returns:
        _type_: value
    """
    while True:
        value = input(f"Enter the value for {key}:")
        if key != "GITHUB_AUTH_TOKEN" and not os.path.exists(value):
            print("[bold red]Alert! [green]Path " +
                  f"[yellow]{value} [green]does not exist")
        else:
            break
    return value

def check_if_value_empty():
    """Checks if any env var is empty. Calls function prompt_user if empty
    """
    user_home = os.path.expanduser('~')
    vars_dir_path = f"{user_home}/.bes-dev-kit"
    vars_file_path = f"{vars_dir_path}/bes-dev-kit.json"
    with open(vars_file_path, 'r+', encoding="utf-8") as file_pointer:
        env_vars = json.load(file_pointer)
        for key, value in env_vars.items():
            if value == "":
                new_value = prompt_user(key, value)
                env_vars[key] = new_value
        file_pointer.seek(0)
        file_pointer.write(json.dumps(env_vars, indent=4))

def set_env_vars():
    """Adds the env env_vars to os.environment
    """
    user_home = os.path.expanduser('~')
    vars_dir_path = f"{user_home}/.bes-dev-kit"
    vars_file_path = f"{vars_dir_path}/bes-dev-kit.json"
    with open(vars_file_path, 'r', encoding="utf-8") as file_pointer:
        env_vars = json.load(file_pointer)
    for key, value in env_vars.items():
        os.environ[key] = str(value)


app = typer.Typer()
generate_app = typer.Typer()
app.add_typer(generate_app, name="generate")


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@generate_app.command("metadata")
def ossp(
    issue_id: int = typer.Option(None, prompt="Enter OSSP id", help="OSSP id"),
    name: str = typer.Option(None, prompt="Enter OSSP name", help="OSSP name"),
    overwrite: bool = typer.Option(False, help="Overwrite the existing entries")
    ):
    """ Update OSSP-master.json file and add/update version file to osspoi datastore """
    write_env_vars_file()
    check_if_value_empty()
    set_env_vars()
    ossp_data = OSSPMaster(issue_id, name)
    ossp_data.generate_ossp_master(overwrite)
    version_data = Version(issue_id, name)
    version_data.generate_version_data(overwrite)


@generate_app.command("report")
def report(
    reports: List[str] = typer.Argument(None),
    get_all: bool = typer.Option(False, help="Get all 3 reports"),
    issue_id: int = typer.Option(None, prompt="Enter OSSP id", help="OSSP id"),
    name: str = typer.Option(None, prompt="Enter OSSP name", help="OSSP name"),
    version: str = typer.Option(None, prompt="Enter version", help="Version of OSSP"),
    update_version_file: bool = typer.Option(True, help="Update scores to version file"),
    ):
    """ Following reports can be generated - scorecard, criticality_score, codeql"""
    write_env_vars_file()
    check_if_value_empty()
    set_env_vars()
    if get_all:
        assessment_reports = ["scorecard", "criticality_score", "codeql"]
        for i in assessment_reports:
            obj = Report(issue_id, name, version, i)
            obj.main()
            if update_version_file and i != "codeql":
                obj.update_version_data()
        raise typer.Exit()
    if len(reports) > 3:
        print("[bold red]Alert! [green]Too many arguments")
        raise typer.Exit()
    for i in reports:
        if i == "scorecard":
            scorecard_obj = Report(issue_id, name, version, i)
            scorecard_obj.main()
            if update_version_file:
                scorecard_obj.update_version_data()
        elif i == "criticality_score":
            criticality_obj = Report(issue_id, name, version, i)
            criticality_obj.main()
            if update_version_file:
                criticality_obj.update_version_data()
        elif i == "codeql":
            codeql_obj = Report(issue_id, name, version, i)
            codeql_obj.main()
        else:
            print(f"[red bold]Alert! [yellow]Invalid report [green]{i}")
            raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
):
    """Callback function for version
    """
    return
