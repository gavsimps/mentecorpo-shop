import sqlite3
from app import app

connection = sqlite3.connect('apparel.db')
cursor = connection.cursor()

connection.close()