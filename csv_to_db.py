import sqlite3
import os
import pandas as pd


def csv_to_db(folder_name, db_name, table_name):
    csv_file_path = folder_name + "/" + table_name
    table_name = os.path.basename(table_name).split('.')[0]

    # Create a new SQLite database (or connect to an existing one)
    conn = sqlite3.connect(db_name)

    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)

    # Convert DataFrame to SQL table
    df.to_sql(table_name, conn, if_exists='replace', index=False)

    # Close the connection
    conn.close()


folder_name = 'HRS_biometric'
table_name = 'Health_Synthetic.csv'
db_name = 'hrs_biometric.db'

csv_to_db(folder_name, db_name, table_name)
