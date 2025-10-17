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
    sql = """SELECT * FROM merchandise WHERE featured = 1"""
    cur = get_db().cursor()
    cur.execute(sql)
    result = cur.fetchall()
    cur.close()
    return result

def get_all():
    sql = """SELECT * FROM merchandise"""
    cur = get_db().cursor()
    cur.execute(sql)
    result = cur.fetchall()
    cur.close()
    return result

def get_item(item_id):
    sql = """SELECT * FROM merchandise WHERE id = %s"""
    cur = get_db().cursor()
    cur.execute(sql, (item_id))
    result = cur.fetchall()
    cur.close()
    return result