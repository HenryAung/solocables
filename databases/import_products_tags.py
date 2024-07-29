import Scripts.databases.dbQueries as dbQueries
import os 
import pandas as pd

dir_path = os.path.dirname(os.path.realpath(__file__))
db_file = os.path.join(dir_path, "business_automation.db")
csv_file = os.path.join(dir_path, "local_df_for_current_rms_dev.csv")
conn = dbQueries.create_connection(db_file)

def fetch_product_group(conn): 
    """ Query distinct product groups """
    cur = conn.cursor()
    sql = "SELECT id_dev, product_group FROM Products"
    cur.execute(sql)
    rows = cur.fetchall()
    return rows

def fetch_tags (conn): 
    """ Query distinct tags """
    cur = conn.cursor()
    sql = "SELECT tag_id, tag_name FROM Tags"
    cur.execute(sql)
    rows = cur.fetchall()
    return rows

def insert_products_tags(conn, id_dev, tag_id):
    """ Insert product tags into the ProductTags table """
    sql = '''
    INSERT INTO ProductTags (id_dev, tag_id)
    VALUES (?, ?)
    '''
    cur = conn.cursor()
    cur.execute(sql, (id_dev, tag_id))
    conn.commit()
    print("Product tags inserted successfully")


def import_products_tags(conn):
    if conn: 
        # Fetch Product Group values and id_dev from the database
        product_groups = fetch_product_group(conn)

        # Fetch tag_names and tag_ids from the local database
        tag_names = fetch_tags(conn)

        # Create a dictionary for quick lookup of tag_id by tag_name
        tag_dict = {tag_name: tag_id for tag_id, tag_name in tag_names}

        # Match Product Group values with tag_names and insert into ProductTags table
        for id_dev, product_group in product_groups:
            if product_group in tag_dict:
                tag_id = tag_dict[product_group]
                insert_products_tags(conn, id_dev, tag_id)

        # Close the connection
        conn.close()

def fetch_product_by_id(conn, id_dev):
    """ Query product by id_dev """
    """ Query distinct product names """
    cur = conn.cursor()
    sql = "SELECT id_dev, name FROM Products where id_dev = ?"
    cur.execute(sql, (id_dev,))
    rows = cur.fetchall()
    return rows

def fetch_tags_by_id(conn, tag_id):
    """ Query tags by id_dev """
    cur = conn.cursor()
    sql = "SELECT tag_id, tag_name FROM Tags WHERE tag_id = ?"
    cur.execute(sql, (tag_id,))
    rows = cur.fetchall()
    return rows

product = fetch_product_by_id(conn, 1057)
tag = fetch_tags_by_id(conn, 207)
print(product, tag)