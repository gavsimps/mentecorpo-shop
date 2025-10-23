# import sqlite3
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

db = SQLAlchemy()

###################### SQL OBJECT MODELS ##################
class Merchandise(db.Model):
    __tablename__ = 'merchandise'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    # file path to image ---> "images/newUS.png"
    image = db.Column(db.String(500))
    # top (t) or bottom (b) or misc (m)
    product_tb = db.Column(db.String(1), nullable=False)
    # long sleeve, v-cut, shorts, etc
    product_type = db.Column(db.String(100))
    # xs, s, m, l, xl, xxl, xxxl
    size = db.Column(db.String(5))
    color = db.Column(db.String(15))
    price = db.Column(db.DECIMAL(6,2), nullable=False)
    in_stock = db.Column(db.Boolean, default=False)
    amount_sold = db.Column(db.Integer) 
    featured = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.Date, default=date.today)