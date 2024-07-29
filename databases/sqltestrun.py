import Scripts.databases.dbQueries as dbQueries
import Scripts.databases.tagDbQueries as tagDbQueries
import os 
import pandas as pd


dir_path = os.path.dirname(os.path.realpath(__file__))
db_file = os.path.join(dir_path, "business_automation.db")
csv_file = os.path.join(dir_path, "local_df_for_current_rms_dev.csv")


conn = dbQueries.create_connection(db_file)



product = dbQueries.select_product_by_id(conn, 1724)
print(product)

# products = dbQueries.select_product_by_tagID(conn, 152)
# print(products)

# id_devs = [1724, 1725, 1726]
# for number in id_devs:
#     dbQueries.update_Product_tag(conn, number, 209)




# tag = tagDbQueries.select_tag_by_id(conn, 153)
# print(tag)

# tag = tagDbQueries.select_tag_by_name(conn, 'DJ Kit - Accessories')
# print(tag)

# tagDbQueries.insert_tags(conn, 'Catridges')

# tagDbQueries.update_tag(conn, (, 122))

# 