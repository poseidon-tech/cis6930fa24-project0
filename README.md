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


## Demo video

[watch](https://github.com/user-attachments/assets/1f953741-2846-47ea-8fd6-b4bb01a6d4bd)



## Folder Structure
```
|   COLLABORATORS.md
|   Pipfile
|   Pipfile.lock
|   README.md
|   setup.cfg
|   setup.py
|
+---project0
|       main.py
|
+---resources
|       test_data.pdf
|
\---tests
        test_main.py
```

- **COLLABORATORS.md:** Contains information about collaborators and a list of resources used for the assignment.
- **main.py:** This is the main python file where the business logic resides, it Processes command-line arguments to either fetch Incidents data from the URL provided by user.
- **Pipfile:** Manages the Python virtual environment and lists all dependencies.
- **Pipfile.lock:** Specifies the versions of dependencies to ensure consistent environments.
- **README.md:** This file, which documents the assignment.
- **setup.cfg** and **setup.py:** Used for setting up the Python environment.
- **docs:** Contains documentation for the assignment.
- **LICENSE:** Contains licensing information, including copyright, publishing, and usage rights.
- **Resources:** Stores data files, including `test_data.pdf`, which is a sample pdf for testing.
- **tests:** Contains test files. `test_main.py` is used for testing the main Python file.

## `main.py`

**Functions in `main.py`:**

### `main(url)`
This function manages the complete workflow by retrieving incident data from the given URL, extracting the relevant incidents, creating a database, populating it, and displaying the status.


### `fetch_incidents(url)`
This function takes a URL as an argument, calls the Norman police API to retrieve the pdf and saves it in resources folder, and returns the the name of pdf file as well as status code.

### `create_db()`
This function creates database and save the database as normanpd.db in resources folder. It also creates empty table with Incident schema (Date/Time, Incident Number, Location
, Nature
, Incident ORI)

### `extract_incidents(pdf_path)`
This function takes name of pdf file as input argument. It cleans the data and extracts the incident information into a data frame, It returns the data frame

### `parse_lines(lines, incident_pattern, location_pattern)`
This is a helper function for `extract_incident(pdf_path)` ,It calls other functions to clean the data and returns the extracted data in a list format to the called function.

### `skip_text(line)`
This is a helper funtion for `parse_lines(lines, incident_pattern, location_pattern)` used to skip unwanted lines that contains text such "Daily incident summary" or "Norman Police Department".

### `process_multiline(lines, line, index):`
This is a helper funtion for `parse_lines(lines, incident_pattern, location_pattern)` used to solve the edge case when a single incident data lies in two rows.

### `status(db)`
The `status(db)` function outputs to standard output a list of incident types and their corresponding occurrence counts. The list is sorted alphabetically and case-sensitively by the incident type

## `test_main.py`

**Functions in `test_main.py`:**

### `test_fetch_incidents()`
Tests whether the PDF is downloaded successfully and is not empty.

### `test_extract_incidents()`
Tests whether incidents are extracted correctly into a Pandas DataFrame. It checks for the datatype and length of data frame.

### `test_skip_text()`
Tests whether unwanted lines are skipped or not.

### `test_create_db()`
Tests whether the daatabase is created and also tests for creation empty incidents table.

### `test_populate_db()`
Tests whether the database is populated with incident data.

### `test_status_output()`
Checks whether the printed output matches expected values .

## Bugs and Assumptions

- There are some Assumptions I made based on data I observed in couple of pdf files, If pdf structure consistency changes then require adjustments to the extraction logic.
- Data on Norman Police page changes daily, so testing with an old downloaded file may result in errors.
- Calling API too frequently results in temporary ban of client.
- Users running this code may encounter errors if there are compatibility issues with the installed dependencies.
