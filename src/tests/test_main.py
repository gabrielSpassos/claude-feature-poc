import builtins
import calendar
from datetime import date
from unittest.mock import patch

from click.testing import CliRunner

import hours.main as main


def make_datasource(data):
    return patch("hours.main.datasource.get_or_create_datasource", return_value=data)

def update_datasource_mock():
    return patch("hours.main.datasource.update_datasource")


def test_cli_welcome_existing_user():
    runner = CliRunner()

    datasource_data = {
        "name": "Gabriel",
        "last_name": "Passos",
        "contract_hours": 160
    }

    with make_datasource(datasource_data):
        result = runner.invoke(main.cli)

    assert "Welcome back, Gabriel Passos!" in result.output
    assert "Contract hours per month: 160" in result.output


def test_cli_setup_user_data():
    runner = CliRunner()

    with make_datasource({}), \
         update_datasource_mock() as update_mock:

        result = runner.invoke(
            main.cli,
            input="Gabriel\nPassos\n160\n"
        )

    assert result.exit_code == 0
    assert update_mock.called
    assert "Setup hours tracker done successfully." in result.output


def test_working_days_in_current_month():
    with patch("hours.main.date") as mock_date:
        mock_date.today.return_value = date(2025, 1, 15)
        mock_date.side_effect = lambda *args, **kw: date(*args, **kw)

        days = main.working_days_in_current_month()
        assert days == 23


def test_get_hours_per_day():
    runner = CliRunner()

    with patch("hours.main.date") as mock_date:
        mock_date.today.return_value = date(2025, 1, 10)
        mock_date.side_effect = lambda *args, **kw: date(*args, **kw)

        with make_datasource({"contract_hours": 160}):
            result = runner.invoke(main.get_hours_per_day)

    assert result.exit_code == 0
    assert "You need to work" in result.output
    assert "6.96" in result.output

