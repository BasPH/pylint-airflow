<img style="float: right;" src="images/pylint-airflow.png">

# pylint-airflow

[![Code style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/BasPH/airflow-examples/blob/master/LICENSE)

Pylint plugin for static code analysis on Airflow code.

## Usage

Installation:
```bash
......
```

Usage:
```bash
pylint --load-plugins=pylint_airflow [your_file]
```

This plugin runs on Python 3.6 and higher.

## Error codes
The Pylint-Airflow codes follow the structure `{I,C,R,W,E,F}83{0-9}{0-9}`, where:

- The characters show:
    - `I` = Info
    - `C` = Convention
    - `R` = Refactor
    - `W` = Warning
    - `E` = Error
    - `F` = Fatal
- `83` is the base id (see all here https://github.com/PyCQA/pylint/blob/master/pylint/checkers/__init__.py)
- `{0-9}{0-9}` is any number 00-99

The current codes are:

| Code  | Symbol                            | Description                                                                                                                                                     |
|-------|-----------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| C8300 | different-operator-varname-taskid | For consistency assign the same variable name and task_id to operators.                                                                                         |
| C8301 | match-callable-taskid             | For consistency name the callable function '_[task_id]', e.g. PythonOperator(task_id='mytask', python_callable=_mytask).                                        |
| C8302 | mixed-dependency-directions       | For consistency don't mix directions in a single statement, instead split over multiple statements.                                                             |
| C8303 | task-no-dependencies              | Sometimes a task without any dependency is desired, however often it is the result of a forgotten dependency.                                                   |
| R8300 | unused-xcom                       | Return values from a python_callable function or execute() method are automatically pushed as XCom.                                                             |
| W8300 | basehook-top-level                | Airflow executes DAG scripts periodically and anything at the top level of a script is executed. Therefore, move BaseHook calls into functions/hooks/operators. |
| E8300 | duplicate-dag-name                | DAG name should be unique.                                                                                                                                      |
| E8301 | duplicate-task-name               | Task name within a DAG should be unique.                                                                                                                        |
| E8302 | duplicate-dependency              | Task dependencies can be defined only once.                                                                                                                     |
| E8303 | dag-with-cycles                   | A DAG is acyclic and cannot contain cycles.                                                                                                                     |

## Documentation

Documentation is available on Read the Docs. TODO: make docs, upload, and make link here.

## Contributing

Suggestions for more checks are always welcome, please create an issue on GitHub. Read CONTRIBUTING.md for more details.

# TODO:
- check if top level code
- check if params supplied via operator args exist