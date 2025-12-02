# Claude Code Implementing Features

> This is a CLI project to track working hours

### Prompts

1.
```
1. Add feature where when the datasource.json is created we will have a new atribute called as "worked_hours", this attribute should be a map where the key should be a date on format of yyyy-MM and the value of the map should be other map, this other map should be with keys as the current month dates on format yyyy-MM-dd and the value should be by default 0.
2. Add this code to the main.py collect_user_data method
3. Do this fast
4. Not run tests
```

2.
```
1. Add a new @click.command named as "edit-worked-hours" where user can edit the worked_hours passing two params: day on format yyyy-MM-dd and an number of how many hours the person worked, if on "worked_hours" datasource the key yyyy-MM does not exist yet, please fill with same logic that was done previously.
2. Update the get_hours_per_day to calculate the hours that was already worked based on the "worked_hours" values and outputs how many hours left until completes the contract hours and also how much the person should do per day, also continue displaying how much was the initial estimative of how many hours the person should do per day.
3. Do this fast
4. Not run tests
```

3. 
```
1. Add a new @click.command named as "backfill-worked-hours". This command should access url from the .variable `timesheet_url` where the date is on format yyyy-MM-dd and should access twice the system based on current month, first with the data was yyyy-MM-15 and then yyyy-MM-16. Inside the system will be a table, will exist a row labled with "Total Hours" and for each day backfill the "worked_hours" with the value from the UI.
2. Do this fast
3. Not run tests
```

### Usage

* Create virtual env
```
python3 -m venv .venv
. .venv/bin/activate
```

* Deactivate virtual env
```
deactivate
```

* Install dependencies
```
pip3 install -r requirements.txt
```

* Install executable
```
pip3 install -e .
```

* Run executable
```
hours
```

* Run Manually
```
python3 src/hours/main.py
```