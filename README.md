# CIS6930FA24 -- Project 0

**Name:** Prajay Yalamanchili

## Project Description

The aim of this project is to extract incident data from a PDF file provided by the Norman Police Department, process the extracted information, store it in a SQLite database, and print a status summary of incidents by nature.

## How to Install

**For Windows:**

1. If Python is not already installed on your system, download and install Python version 3.12 from [here](https://www.python.org/downloads/).
2. Set your path in the environment variables. To learn how to set the path in environment variables, read this [article](https://www.liquidweb.com/help-docs/adding-python-path-to-windows-10-or-11-path-environment-variable/).
3. Download or clone this repository.
4. Navigate to the project directory on your local machine.
5. Run the following commands:

    ```bash
    pip install pipenv
    ```
    ```bash
    pipenv install
    ```

## How to Run

To execute the `main.py` file, use:
```bash
pipenv run python project0/main.py --incidents URL_TO_PDF
```
To run tests, use:
```bash
pipenv run python -m pytest -v
```
or

```bash
pipenv run pytest
```