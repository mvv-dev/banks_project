# World’s Largest Banks ETL Pipeline

This project implements an automated **ETL pipeline** to collect, process, and store information about the world’s largest banks by market capitalization.

The pipeline extracts data from an archived Wikipedia page, converts the market capitalization values from USD into GBP, EUR, and INR, and stores the processed data in both CSV and SQLite formats.

## Project Objective

The objective of this project is to build a reusable data pipeline that can be executed periodically to generate an updated report containing the ten largest banks in the world by market capitalization.

## ETL Process

### Extract

The pipeline extracts the following information from the table under the **“By market capitalization”** section:

* Bank name
* Market capitalization in USD billions

### Transform

Exchange rates are loaded from an external CSV file.

The pipeline calculates each bank’s market capitalization in:

* USD
* GBP
* EUR
* INR

All converted values are rounded to two decimal places.

### Load

The transformed data is stored in:

* A CSV file
* A SQLite database table

The pipeline also records its execution progress in a log file.

## Technologies

* Python
* Pandas
* BeautifulSoup
* Requests
* SQLite
* Datetime

## Project Structure

```text
largest-banks-etl/
│
├── banks_project.py
├── Largest_banks_data.csv
├── Banks.db
├── code_log.txt
├── exchange_rate.csv
├── README.md
└── .gitignore
```

## Data Sources

The bank data is extracted from an archived Wikipedia page containing a ranking of the world’s largest banks by market capitalization.

Exchange rates are provided through a CSV file containing conversion rates from USD to other currencies.

## Output Data

The final dataset contains the following columns:

| Column           | Description                           |
| ---------------- | ------------------------------------- |
| `Name`           | Bank name                             |
| `MC_USD_Billion` | Market capitalization in USD billions |
| `MC_GBP_Billion` | Market capitalization in GBP billions |
| `MC_EUR_Billion` | Market capitalization in EUR billions |
| `MC_INR_Billion` | Market capitalization in INR billions |

## Output Files

| File                     | Description                                       |
| ------------------------ | ------------------------------------------------- |
| `Largest_banks_data.csv` | Processed bank data in CSV format                 |
| `Banks.db`               | SQLite database containing the processed data     |
| `code_log.txt`           | Execution logs for each stage of the ETL pipeline |

The processed data is stored in the following database table:

```text
Largest_banks
```

## Pipeline Functions

The application is divided into the following functions:

| Function         | Responsibility                                            |
| ---------------- | --------------------------------------------------------- |
| `log_progress()` | Records the pipeline execution stages                     |
| `extract()`      | Extracts bank data from the webpage                       |
| `transform()`    | Converts market capitalization into additional currencies |
| `load_to_csv()`  | Saves the transformed data to a CSV file                  |
| `load_to_db()`   | Loads the data into a SQLite database                     |
| `run_queries()`  | Executes SQL queries against the database                 |

## How to Run

Install the required dependencies:

```bash
pip install pandas requests beautifulsoup4
```

Run the project:

```bash
python banks_project.py
```

After execution, the CSV file, SQLite database, and log file will be generated in the project directory.

## Example SQL Queries

The project can execute queries such as:

```sql
SELECT *
FROM Largest_banks;
```

```sql
SELECT AVG(MC_GBP_Billion)
FROM Largest_banks;
```

```sql
SELECT Name
FROM Largest_banks
LIMIT 5;
```

## Skills Practiced

* Building an ETL pipeline
* Extracting HTML tables with BeautifulSoup
* Cleaning and transforming data with Pandas
* Reading exchange rates from CSV files
* Writing data to CSV
* Working with SQLite databases
* Executing SQL queries with Python
* Implementing pipeline logging
* Organizing a Python data engineering project

## Acknowledgements

This project was developed as part of the IBM Data Engineering Professional Certificate hands-on labs.
