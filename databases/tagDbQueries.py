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

def select_tag_by_id_dev(conn, id_dev):
    """ Query tags by id_dev """
    cur = conn.cursor()
    sql = '''
    SELECT pt.id_dev, t.tag_id, t.tag_name
    FROM ProductTags pt 
    JOIN Tags t ON pt.tag_id = t.tag_id
    WHERE pt.id_dev = ?
    '''
    cur.execute(sql, (id_dev,))
    
    row = cur.fetchall()
    return row

def select_tag_by_name(conn, tag_name):
    """ Query tags by tag_name """
    cur = conn.cursor()
    cur.execute("SELECT * FROM Tags WHERE tag_name = ?", (tag_name,))
    row = cur.fetchall()
    return row

def update_tag(conn, tag_name, tag_id):
    """ Update tag information """
    sql = '''
    UPDATE Tags
    SET tag_name = ?
    WHERE tag_id = ?
    '''
    try:
        cur = conn.cursor()
        cur.execute(sql, (tag_name, tag_id))
        conn.commit()
        print("Tag updated successfully")
    except Error as e:
        print(f"Error: {e}")