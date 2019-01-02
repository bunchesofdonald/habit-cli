from datetime import date, timedelta
from terminaltables import AsciiTable
import click
import json
import os

CONFIG_PATH = os.path.expanduser("~/.config/habit-cli/")
EMPTY_HABIT_DATA = {"habits": [], "log": {}}


def save_habit_data(data):
    if not os.path.exists(CONFIG_PATH):
        os.makedirs(CONFIG_PATH)
    with open(os.path.join(CONFIG_PATH, "data.json"), "w") as outfile:
        json.dump(data, outfile, sort_keys=True, indent=4)


def load_habit_data():
    try:
        with open(os.path.join(CONFIG_PATH, "data.json")) as infile:
            return json.load(infile)
    except FileNotFoundError:
        return EMPTY_HABIT_DATA


def get_log_date(yesterday=False):
    if yesterday:
        return (date.today() - timedelta(days=1)).isoformat()
    else:
        return date.today().isoformat()


@click.group()
def cli():
    pass


@cli.command()
@click.argument("habit")
def add(habit):
    """Add a habit to track"""
    data = load_habit_data()
    if habit not in data["habits"]:
        data["habits"].append(habit.lower())
        data["habits"].sort()
        save_habit_data(data)


@cli.command()
def list():
    """List all known habits"""
    data = load_habit_data()
    table_data = [["habits"]]
    for habit in data["habits"]:
        table_data.append([habit.title()])

    click.echo(AsciiTable(table_data).table)


@cli.command()
@click.option("--yesterday", "-y", is_flag=True, help="Log habit to yesterday's log.")
@click.argument("habit")
def log(habit, yesterday):
    """Mark a habit as complete for the day"""
    data = load_habit_data()
    habit = habit.lower()
    try:
        data["habits"].index(habit)
    except ValueError:
        # Check for partial habit name match
        possibles = []
        for known in data["habits"]:
            if known.startswith(habit):
                possibles.append(known)

        if len(possibles) == 0:
            raise click.ClickException(
                f"No habit found matching {click.style(habit, fg='yellow')}. "
                f"You can add it with: `hb add {habit}`."
            )
        elif len(possibles) > 1:
            raise click.ClickException(
                f"{click.style(habit, fg='yellow')} is ambiguous, found "
                f"multiple matching habits: {possibles}."
            )
        else:
            habit = possibles[0]

    log_date = get_log_date(yesterday)

    if log_date not in data["log"]:
        data["log"][log_date] = []

    if habit not in data["log"][log_date]:
        data["log"][log_date].append(habit)

    save_habit_data(data)
    click.echo(f"Logged habit {click.style(habit, fg='yellow')} for {log_date}.")


@cli.command()
@click.option("--yesterday", "-y", is_flag=True, help="Show yesterday's log.")
def show(yesterday=False):
    """Show progress on habits for the day"""
    data = load_habit_data()
    log_date = get_log_date(yesterday)

    table_data = [["", "habit"]]
    for habit in data["habits"]:
        if log_date in data["log"]:
            state = "✓" if habit in data["log"][log_date] else "✕"
        else:
            state = "✕"

        table_data.append([state, habit.title()])

    click.echo(AsciiTable(table_data, title=log_date).table)
