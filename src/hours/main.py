import os
import calendar
import csv
from datetime import date, datetime
from pathlib import Path
import click
import hours.datasource as datasource

LOGO = click.style(r"""
██╗  ██╗ ██████╗ ██╗   ██╗██████╗ ███████╗
██║  ██║██╔═══██╗██║   ██║██╔══██╗██╔════╝
███████║██║   ██║██║   ██║██████╔╝███████╗
██╔══██║██║   ██║██║   ██║██╔══██╗╚════██║
██║  ██║╚██████╔╝╚██████╔╝██║  ██║███████║
╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚══════╝
""", fg="bright_cyan")


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        click.echo(LOGO)
        welcome_display()
        click.echo(ctx.get_help())


def welcome_display():
    datasource_data = datasource.get_or_create_datasource()
    if "name" in datasource_data and "last_name" in datasource_data and "contract_hours" in datasource_data:
        name = datasource_data["name"]
        last_name = datasource_data["last_name"]
        click.echo(f"Welcome back, {name} {last_name}!")
        click.echo(f"Contract hours per month: {datasource_data['contract_hours']}")
    else:
        click.echo("Welcome! Let's set up your hours tracker.")
        collect_user_data.main(args=[], standalone_mode=False)
        click.echo("Thank You! Setup hours tracker done successfully.")


@click.command()
@click.option('--name', prompt='Your name', help='The name to store.')
@click.option('--last-name', prompt='Your last name', help='The last name to store.')
@click.option('--contract-hours', type=int, prompt='Your contract monthly hours', help='The contract hours per month to store.')
def collect_user_data(name, last_name, contract_hours):
    today = datetime.now()
    year_month = today.strftime("%Y-%m")

    days_in_month = calendar.monthrange(today.year, today.month)[1]
    month_dates = {
        f"{today.year}-{today.month:02d}-{day:02d}": 0
        for day in range(1, days_in_month + 1)
    }

    worked_hours = {
        year_month: month_dates
    }

    data = {
        "name": name,
        "last_name": last_name,
        "contract_hours": contract_hours,
        "worked_hours": worked_hours
    }
    datasource.update_datasource(data)


@click.command()
@click.option('--day', prompt='Day (yyyy-MM-dd)', help='The day to edit worked hours.')
@click.option('--hours', type=float, prompt='Hours worked', help='The number of hours worked.')
def edit_worked_hours(day, hours):
    datasource_data = datasource.get_or_create_datasource()

    year_month = day[:7]

    if "worked_hours" not in datasource_data:
        datasource_data["worked_hours"] = {}

    if year_month not in datasource_data["worked_hours"]:
        year, month = map(int, year_month.split('-'))
        days_in_month = calendar.monthrange(year, month)[1]
        month_dates = {
            f"{year}-{month:02d}-{d:02d}": 0
            for d in range(1, days_in_month + 1)
        }
        datasource_data["worked_hours"][year_month] = month_dates

    datasource_data["worked_hours"][year_month][day] = hours
    datasource.update_datasource(datasource_data)
    click.echo(f"Updated {day} with {hours} hours worked.")


@click.command()
def get_hours_per_day():
    datasource_data = datasource.get_or_create_datasource()

    if "contract_hours" not in datasource_data:
        collect_user_data.main(args=[], standalone_mode=False)

    contract_hours = datasource_data["contract_hours"]
    working_days = working_days_in_current_month()
    initial_hours_per_day = contract_hours / working_days

    worked_hours_total = 0
    today = date.today()
    year_month = today.strftime("%Y-%m")

    if "worked_hours" in datasource_data and year_month in datasource_data["worked_hours"]:
        worked_hours_total = sum(datasource_data["worked_hours"][year_month].values())

    hours_remaining = contract_hours - worked_hours_total

    current_day = today.day
    remaining_working_days = sum(
        1
        for week in calendar.monthcalendar(today.year, today.month)
        for day in week[:5]
        if day >= current_day and day != 0
    )

    hours_per_day_remaining = hours_remaining / remaining_working_days if remaining_working_days > 0 else 0

    click.echo(f"Initial estimate: {initial_hours_per_day:.2f} hours per day during {working_days} working days.")
    click.echo(f"Hours worked: {worked_hours_total:.2f} hours")
    click.echo(f"Hours remaining: {hours_remaining:.2f} hours")
    click.echo(
        f"You need to work {hours_per_day_remaining:.2f} hours per day during the remaining {remaining_working_days} working days "
        f"to meet your contract of {contract_hours} hours this month."
    )



def working_days_in_current_month():
    today = date.today()
    year, month = today.year, today.month
    
    month_calendar = calendar.monthcalendar(year, month)
    
    working_days = sum(
        1
        for week in month_calendar
        for day in week[:5]
        if day != 0
    )
    
    return working_days


@click.command()
@click.option('--month', prompt='Month (yyyy-MM)', help='The month to export hours.')
def export_hours(month):
    datasource_data = datasource.get_or_create_datasource()

    if "contract_hours" not in datasource_data:
        click.echo("No contract hours found. Please setup your data first.")
        return

    contract_hours = datasource_data["contract_hours"]
    year, month_num = map(int, month.split('-'))

    working_days = sum(
        1
        for week in calendar.monthcalendar(year, month_num)
        for day in week[:5]
        if day != 0
    )

    expected_hours_per_day = contract_hours / working_days if working_days > 0 else 0

    worked_hours_total = 0
    if "worked_hours" in datasource_data and month in datasource_data["worked_hours"]:
        worked_hours_total = sum(datasource_data["worked_hours"][month].values())

    hours_left = contract_hours - worked_hours_total

    today = date.today()
    current_year_month = today.strftime("%Y-%m")

    if month == current_year_month:
        current_day = today.day
        remaining_working_days = sum(
            1
            for week in calendar.monthcalendar(year, month_num)
            for day in week[:5]
            if day >= current_day and day != 0
        )
    else:
        remaining_working_days = working_days

    current_expectation = hours_left / remaining_working_days if remaining_working_days > 0 else 0

    base_dir = Path(__file__).resolve().parent.parent
    resources_dir = base_dir / "resources"
    csv_path = resources_dir / f"hours_report_{month}.csv"

    with open(csv_path, "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Month", "Contract Hours", "Expected Hours Per Day", "Hours Worked", "Hours Left", "Current Expectation Per Day"])
        writer.writerow([month, contract_hours, f"{expected_hours_per_day:.2f}", f"{worked_hours_total:.2f}", f"{hours_left:.2f}", f"{current_expectation:.2f}"])

    click.echo(f"Report exported to {csv_path}")


cli.add_command(get_hours_per_day)
cli.add_command(edit_worked_hours)
cli.add_command(export_hours)


if __name__ == "__main__":
    cli()
