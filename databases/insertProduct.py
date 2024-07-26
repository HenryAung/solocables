import Scripts.databases.dbQueries as dbQueries
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

db_file = os.path.join(dir_path, "business_automation.db")
csv_file = os.path.join(dir_path, "local_df_for_current_rms_dev.csv")

conn = dbQueries.create_connection(db_file)

# Define the product values



# Insert the product
if conn:
    dbQueries.insert_all_products(conn, db_file, csv_file)

    # Close the connection
if conn:
    conn.close()