# CIS6930FA24 -- Project 0

**Name:** Prajay Yalamanchili

## Project Description

- The aim of this project is to extract incident data from a PDF file provided by the Norman Police Department, process the extracted information, store it in a SQLite database, and print a status summary of incidents by nature in Ascending order.
- The following fields will be extracted and stored in database - `Date / Time` `Incident Number` `Location` `Nature` `Incident ORI`

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
|   LICENSE
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
This function takes a URL as an argument, calls the Norman Police API to retrieve the PDF, saves it in the resources folder, and returns the name of the PDF file along with the status code.

### `create_db()`
This function creates a database and saves it as `normanpd.db` in the resources folder. It also creates an empty table with the Incident schema (Date/Time, Incident Number, Location, Nature, Incident ORI).

### `extract_incidents(pdf_filepath)`
This function takes the name of the PDF file as an input argument, cleans the data, and extracts the incident information into a DataFrame. It returns the DataFrame.

### `parse_lines(row)`
This is a helper function for `extract_incidents(pdf_filepath)`. It uses regex to extract individual fields from string. It returns a list consisting of extracted information.

### `check_page(page)`
This is a helper function for `extract_incidents(pdf_filepath)`. It returns True if page is not empty else returns False.

### `status(db)`
The `status(db)` function outputs a list of incident types and their corresponding occurrence counts to the standard output. The list is sorted alphabetically and case-sensitively by incident type.

## `test_main.py`

**Functions in `test_main.py`:**

### `test_fetch_incidents()`
Tests whether the PDF is downloaded successfully by passing the URL to `fetch_incidents(url)` and checking the status code.

### `test_extract_incidents()`
Tests whether incidents are extracted correctly into a Pandas DataFrame. It checks the datatype and length of the DataFrame.

### `test_check_page()`
Tests whether `check_page(page)` is returning True when non empty page is passed, otherwise it must return false.

### `test_create_db()`
Tests whether the database is created and also checks for the creation of an empty incidents table.

### `test_populate_db()`
Tests whether the database is populated with incident data.

### `test_status_output()`
Checks whether the printed output matches the expected values.


## Bugs and Assumptions

- Some assumptions were made based on the data observed in a couple of PDF files. If the PDF structure changes, adjustments to the extraction logic will be required.
- The data on the Norman Police page changes daily, so testing with an older downloaded file may result in errors.
- Calling the API too frequently can result in a temporary ban of the client.
- Users running this code may encounter errors if there are compatibility issues with the installed dependencies
