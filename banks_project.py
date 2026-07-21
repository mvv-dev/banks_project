import sqlite3
from datetime import datetime

import pandas as pd
import requests
from bs4 import BeautifulSoup
from pandas import DataFrame


DATA_URL = (
    "https://web.archive.org/web/20230908091635/"
    "https://en.wikipedia.org/wiki/List_of_largest_banks"
)

EXCHANGE_RATE_CSV = (
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/"
    "IBMSkillsNetwork-PY0221EN-Coursera/labs/v2/exchange_rate.csv"
)

LOG_FILE = "code_log.txt"
OUTPUT_CSV = "Largest_banks_data.csv"
DATABASE_NAME = "Banks.db"
TABLE_NAME = "Largest_banks"


def log_process(msg: str) -> None:
    """Log the execution progress of the ETL pipeline."""

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(LOG_FILE, "a", encoding="utf-8") as log_file:
        log_file.write(f"[{timestamp}] {msg}\n")


def extract() -> DataFrame:
    """Extract the largest banks table from the source webpage."""

    log_process("Starting data extraction")

    response = requests.get(DATA_URL, timeout=30)
    response.raise_for_status()

    soup_object = BeautifulSoup(response.text, "html.parser")

    banks_table = soup_object.find("table", class_="wikitable")

    if banks_table is None:
        raise ValueError("Banks table was not found on the source page.")

    banks = []

    for row in banks_table.select("tr"):
        columns = row.select("td")

        if len(columns) < 3:
            continue

        bank = {
            "Name": columns[1].get_text(),
            "MC_USD_Billion": columns[2].get_text(),
        }

        banks.append(bank)

    log_process("Data extraction completed")

    return pd.DataFrame(banks)


def transform(df: DataFrame) -> DataFrame:
    """
    Clean the extracted data and add market capitalization values
    converted to GBP, EUR, and INR.
    """

    log_process("Starting data transformation")

    df["Name"] = (
        df["Name"]
        .str.replace("\n", "", regex=False)
        .str.strip()
    )

    df["MC_USD_Billion"] = (
        df["MC_USD_Billion"]
        .str.replace("\n", "", regex=False)
        .str.strip()
        .astype(float)
    )

    exchange_rate_df = pd.read_csv(EXCHANGE_RATE_CSV)

    rates = (
        exchange_rate_df
        .set_index("Currency")["Rate"]
        .to_dict()
    )

    df["MC_GBP_Billion"] = (
        df["MC_USD_Billion"] * rates["GBP"]
    ).round(2)

    df["MC_EUR_Billion"] = (
        df["MC_USD_Billion"] * rates["EUR"]
    ).round(2)

    df["MC_INR_Billion"] = (
        df["MC_USD_Billion"] * rates["INR"]
    ).round(2)

    log_process("Data transformation completed")

    return df


def load_to_csv(df: DataFrame) -> None:
    """Save the transformed data to a CSV file."""

    log_process("Loading data to CSV")

    df.to_csv(
        OUTPUT_CSV,
        index=False,
    )

    log_process("CSV file created successfully")


def load_to_db(df: DataFrame) -> sqlite3.Connection:
    """Load the transformed data into a SQLite database."""

    log_process(f"Loading data to {DATABASE_NAME}")

    connection = sqlite3.connect(DATABASE_NAME)

    df.to_sql(
        name=TABLE_NAME,
        con=connection,
        if_exists="replace",
        index=False,
    )

    log_process("Database loaded successfully")

    return connection


def run_queries(
    connection: sqlite3.Connection,
    query: str,
) -> None:
    """Execute and display an SQL query."""

    log_process(f"Executing query: {query}")

    result = connection.execute(query)

    for row in result:
        print(row)

    log_process("Query executed successfully")


def main() -> None:
    log_process("ETL pipeline started")

    df = extract()
    df = transform(df)

    load_to_csv(df)

    connection = load_to_db(df)

    try:
        run_queries(
            connection,
            f"SELECT * FROM {TABLE_NAME}",
        )
    finally:
        connection.close()

    log_process("ETL pipeline completed")


if __name__ == "__main__":
    main()