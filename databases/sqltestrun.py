import Scripts.databases.dbQueries as dbQueries
import os 
import pandas as pd


dir_path = os.path.dirname(os.path.realpath(__file__))
db_file = os.path.join(dir_path, "business_automation.db")
csv_file = os.path.join(dir_path, "local_df_for_current_rms_dev.csv")


conn = dbQueries.create_connection(db_file)

dbQueries.delete_table(conn, "Products")