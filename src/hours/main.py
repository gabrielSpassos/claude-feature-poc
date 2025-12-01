import calendar
from datetime import date
import click
import hours.datasource as datasource

LOGO = click.style(r"""
██╗  ██╗ ██████╗ ██╗   ██╗██████╗ ███████╗
██║  ██║██╔═══██╗██║   ██║██╔══██╗██╔════╝
███████║██║   ██║██║   ██║██████╔╝█████╗  
██╔══██║██║   ██║██║   ██║██╔══██╗██╔══╝  
██║  ██║╚██████╔╝╚██████╔╝██║  ██║███████╗
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
    data = {
        "name": name,
        "last_name": last_name,
        "contract_hours": contract_hours
    }
    datasource.update_datasource(data)


@click.command()
def get_hours_per_day():
    datasource_data = datasource.get_or_create_datasource()

    if "contract_hours" not in datasource_data:
        collect_user_data.main(args=[], standalone_mode=False)
    
    contract_hours = datasource_data["contract_hours"]
    working_days = working_days_in_current_month()
    hours_per_day = contract_hours / working_days
    click.echo(
        f"You need to work {hours_per_day:.2f} hours per day during {working_days} working days "
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


cli.add_command(get_hours_per_day)


if __name__ == "__main__":
    cli()
