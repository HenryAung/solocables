import sqlite3
from sqlite3 import Error
import pandas as pd


def create_connection(db_file):
    """ Create a database connection to the SQLite database specified by db_file """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Connected to SQLite database: {db_file}")
    except Error as e:
        print(f"Error: {e}")
    return conn


def create_tables(conn, sql):
    """Create tables in the SQLite database"""
    try:
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        print("Tables created successfully")
    except Error as e:
        print(f"Error: {e}")


def delete_table(conn, table_name):
    """Delete a table from the SQLite database"""
    sql = f"DROP TABLE IF EXISTS {table_name}"
    try:
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        print(f"Table '{table_name}' deleted successfully")
    except Error as e:
        print(f"Error: {e}")


def select_table(conn, tablename):
    """Select all rows from the specified table"""
    sql = f"SELECT * FROM {tablename}"
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        print(row)


def list_tables(conn):
    """List all tables in the database"""
    sql = "SELECT name FROM sqlite_master WHERE type='table';"
    cur = conn.cursor()
    cur.execute(sql)
    tables = cur.fetchall()
    for table in tables:
        print(table[0])

def delete_all_data_from_table(conn, table_name):
    """ Delete all data from the specified table """
    sql = f"DELETE FROM {table_name}"
    try:
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        print(f"All data deleted from table '{table_name}'")
    except Error as e:
        print(f"Error: {e}")

        


def insert_product(conn, product):
    """ Insert a new product into the Products table """
    sql = '''
    INSERT INTO Products (id_dev, id_live, name, product_group, description, mainsPowerReq, powerType, prefPwrCbl, isCable, cblLeng, connector1, connector2, prefPwrCbl_dev)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)
    '''
    try:
        cur = conn.cursor()
        cur.execute(sql, product)
        conn.commit()
        print("Product inserted successfully")
    except Error as e:
        print(f"Error: {e}")


def delete_product(conn, product_id):
    """ Delete a product from the Products table based on id_dev """
    sql = 'DELETE FROM Products WHERE id_dev = ?'
    try:
        cur = conn.cursor()
        cur.execute(sql, (product_id))
        conn.commit()
        print(f"Product with id_dev {product_id} deleted successfully")
    except Error as e:
        print(f"Error: {e}")


def import_all_products(conn, db_file, csv_file):
    """ Load data from CSV file and insert into SQLite database """
    conn = create_connection(db_file)
    if conn:
        # Read CSV file into DataFrame
        df = pd.read_csv(csv_file)
   
        # Iterate over rows and insert each row into the database
        for _, row in df.iterrows():
            product = (
                row.get('id_dev'),  # Assumes CSV column names match table column names
                row.get('id_live'),
                row.get('name'),
                row.get('product_group'),
                row.get('description'),
                row.get('mainsPowerReq'),
                row.get('powerType'),
                row.get('prefPwrCbl'),
                row.get('isCable'),
                row.get('cblLeng'),
                row.get('connector1'),
                row.get('connector2'),
                row.get('prefPwrCbl_dev')
            )
            insert_product(conn, product)
        
        conn.close()


def select_all_products(conn): 
    """ Query all rows in the Products table """
    cur = conn.cursor()
    sql = f"SELECT * FROM Products"
    cur.execute(sql)
    rows = cur.fetchall()
    return rows 

def select_product_by_id(conn, product_id):
    """ Query products by id_dev """
    cur = conn.cursor()
    sql = f"SELECT * FROM Products WHERE id_dev = ?"
    cur.execute(sql, (product_id,))
    row = cur.fetchall()
    return row 


def update_product(conn, product):
    """ Update product information """
    sql = '''
    UPDATE Products
    SET id_live = ?,
        name = ?,
        description = ?,
        mainsPowerReq = ?,
        powerType = ?,
        prefPwrCbl = ?,
        isCable = ?,
        cblLeng = ?,
        connector1 = ?,
        connector2 = ?,
        prefPwrCbl_dev = ?
    WHERE id_dev = ?
    '''
    try:
        cur = conn.cursor()
        cur.execute(sql, product)
        conn.commit()
        print("Product updated successfully")
    except Error as e:
        print(f"Error: {e}")


def delete_product_group_column(conn):
    """ Delete the product_group column from the Products table """
    sql = '''
    CREATE TABLE Products_temp AS
    SELECT id_dev, id_live, name, description, mainsPowerReq, powerType, prefPwrCbl, isCable, cblLeng, connector1, connector2, prefPwrCbl_dev
    FROM Products;
    '''
    try:
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        print("Temporary table created successfully")
    except Error as e:
        print(f"Error: {e}")

    sql = '''
    DROP TABLE Products;
    '''
    try:
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        print("Products table dropped successfully")
    except Error as e:
        print(f"Error: {e}")

    sql = '''
    ALTER TABLE Products_temp
    RENAME TO Products;
    '''
    try:
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        print("Temporary table renamed to Products successfully")
    except Error as e:
        print(f"Error: {e}")


def insert_product_tag(conn, product_tag):
    """ Insert product-tag relationship into the ProductTags table """
    sql = '''
    INSERT INTO ProductTags (product_id, tag_id)
    VALUES (?, ?)
    '''
    try:
        cur = conn.cursor()
        cur.execute(sql, product_tag)
        conn.commit()
        print("Product-Tag relationship inserted successfully")
    except Error as e:
        print(f"Error: {e}")


def select_product_by_tagID(conn, tagID):
    """ Query products by product_group """
    cur = conn.cursor()
    sql = """
    SELECT p.name, p.id_dev, pt.tag_id 
    FROM ProductTags pt 
    JOIN Products p ON pt.id_dev =p.id_dev       
    WHERE pt.tag_id = ?"""
    cur.execute(sql, (tagID,))
    rows = cur.fetchall()
    return rows


def update_Product_tag(conn, id_dev, tag_id):
    """ Update tag information """
    sql = '''
    UPDATE ProductTags
    SET tag_id = ?
    WHERE id_dev = ?
    '''
    try:
        cur = conn.cursor()
        cur.execute(sql, (tag_id, id_dev))
        conn.commit()
        print("Tag updated successfully")
    except Error as e:
        print(f"Error: {e}")
