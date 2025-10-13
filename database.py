import sqlite3
from flask import g

DATABASE = 'db/apparel.db'

# connection = sqlite3.connect("apparel.db")
# crsr = connection.cursor()

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def get_featured():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    sql = """SELECT * FROM merchandise WHERE featured = 1"""
    cursor.execute(sql)
    feat = cursor.fetchall()
    cursor.close()
    return feat