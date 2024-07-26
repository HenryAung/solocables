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
    create_products_table = '''
    CREATE TABLE IF NOT EXISTS Products (
        id_dev INTEGER PRIMARY KEY NOT NULL,
        id_live INTEGER,
        name TEXT(50) NOT NULL UNIQUE,
        product_group TEXT(50),
        description TEXT(255),
        mainsPowerReq INTEGER,
        powerType TEXT(50),
        prefPwrCbl TEXT(25),
        isCable INTEGER,
        cblLeng NUMERIC,
        connector1 TEXT(25),
        connector2 TEXT(25),
        prefPwrCbl_dev TEXT(25)
    );
    '''

  
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

def insert_product(conn, product):
    """ Insert a new product into the Products table """
    sql = '''
    INSERT INTO Products (id_dev, id_live, name, description, mainsPowerReq, powerType, prefPwrCbl, isCable, cblLeng, connector1, connector2, prefPwrCbl_dev)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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

def select_all_products(conn, table_name): 
    """ Query all rows in the Products table """
    cur = conn.cursor()
    sql = f"SELECT * FROM {table_name}"
    cur.execute(sql)
    rows = cur.fetchall()
    return rows 

def select_product_by_id(conn, table_name, product_id):
    """ Query products by id_dev """
    cur = conn.cursor()
    sql = f"SELECT * FROM {table_name} WHERE id_dev = ?"
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

def insert_tags(conn, tags):
    """ Insert tags into the Tags table """
    sql = '''
    INSERT INTO Tags (tag_name)
    VALUES (?)
    '''
    try:    
        cur = conn.cursor()
        cur.execute(sql, (tags,))
        conn.commit()
        print("Tags inserted successfully")
    except Error as e:
        print(f"Error: {e}")

def delete_tag(conn, tag_id):
    """ Delete a tag from the Tags table based on tag_id """
    sql = 'DELETE FROM Tags WHERE tag_id = ?'
    try:
        cur = conn.cursor()
        cur.execute(sql, (tag_id,))
        conn.commit()
        print(f"Tag with tag_id {tag_id} deleted successfully")
    except Error as e:
        print(f"Error: {e}")

def select_all_tags(conn):
    """ Query all rows in the Tags table """
    cur = conn.cursor()
    cur.execute("SELECT * FROM Tags")
    rows = cur.fetchall()
    return rows

def select_tag_by_id(conn, tag_id):
    """ Query tags by tag_id """
    cur = conn.cursor()
    cur.execute("SELECT * FROM Tags WHERE tag_id = ?", (tag_id,))
    row = cur.fetchall()
    return row

def update_tag(conn, tags):
    """ Update tag information """
    sql = '''
    UPDATE Tags
    SET tag_name = ?
    WHERE tag_id = ?
    '''
    try:
        cur = conn.cursor()
        cur.execute(sql, tags)
        conn.commit()
        print("Tag updated successfully")
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