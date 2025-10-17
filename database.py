import sqlite3
from flask import g

DATABASE = 'db/apparel.db'

def get_connection():
    conn = sqlite3.connect(DATABASE)

# connection = sqlite3.connect("apparel.db")
# crsr = connection.cursor()

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def get_featured():
    conn = get_connection()
    sql = """SELECT * FROM merchandise WHERE featured = 1"""
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            feat = cursor.fetchall()
            cursor.close()
            return feat

def get_all():
    conn = get_connection()
    sql = """SELECT * FROM merchandise"""
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            all_items = cursor.fetchall()
            cursor.close()
            return all_items

def get_item(item_id):
    conn = get_connection()
    sql = """SELECT * FROM merchandise WHERE id = %s"""
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (item_id))
            singular = cursor.fetchall()
            cursor.close()
            return singular