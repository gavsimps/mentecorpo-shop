import sqlite3

connection = sqlite3.connect("apparel.db")

# cursor
crsr = connection.cursor()
drop_table = """DROP TABLE merchandise;"""

# SQL command to create a table in the database
sql_command = """CREATE TABLE merchandise ( 
id INTEGER PRIMARY KEY NOT NULL, 
name VARCHAR(100) NOT NULL,
image VARCHAR(100),
product_type VARCHAR(100) NOT NULL,
size VARCHAR(4),
color VARCHAR(10) NOT NULL,
price DECIMAL(6,2) NOT NULL,
in_stock BOOLEAN NOT NULL,
amount_sold INTEGER,
featured BOOLEAN,
date_created DATE);"""

# execute the statement
# crsr.execute(drop_table)
# crsr.execute(sql_command)

def insertClothing(id, name, image, product_type, size, color, price, in_stock, amount_sold, featured, date_created):
    try:
        connection = sqlite3.connect("apparel.db")
        cursor = connection.cursor()
        sqlite_insert_blob_query = """ INSERT INTO merchandise
                                  (id, name, image, product_type, size, color, price, in_stock, amount_sold, featured, date_created) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        # empPhoto = convertToBinaryData(image)
        # data_tuple = (id, name, image, product_type, size, color, price, in_stock, amount_sold, featured, date_created)
        # cursor.execute(sqlite_insert_blob_query, data_tuple)
        cursor.execute(sqlite_insert_blob_query)
        connection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to insert blob data into sqlite table", error)
    finally:
        if connection:
            connection.close()
            print("the sqlite connection is closed")

insertClothing(1, "mario skin suit", "images/newUS.png", "skin", "large", "italian", "4.99", 1, 0, 1, "2025-10-10")
# close the connection
# connection.close()

def get_clothes():
    connection = sqlite3.connect("apparel.db")
    cursor = connection.cursor()
    sql_fetch_blob_query = """SELECT * from merchandise"""
    cursor.execute(sql_fetch_blob_query)
    return cursor.fetchall()

        