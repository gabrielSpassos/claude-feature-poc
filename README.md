# Claude Code Implementing Features

> This is a CLI project to track working hours

### Prompts

1.
```
1. Add this code to the main.py collect_user_data method
2. Add feature where when the datasource.json is created we will have a new atribute called as "worked_hours", this attribute should be a map where the key should be a date on format of yyyy-MM and the value of the map should be other map, this other map should be with keys as the current month dates on format yyyy-MM-dd and the value should be by default 0.
```

2.
```
Add a new @click.command named as "edit-worked-hours" where user can edit the worked_hours passing two params: date on format yyyy-MM-dd and an number of how many hours the person worked.
```

3. 
```
Update the get_hours_per_day to calculate the hours that was already worked based on the "worked_hours" values and outputs how many hours left until completes the contract hours and also how much the person should do per day, also continue displaying how much was the initial estimative of how many hours the person should do per day.
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