from flask import Flask, render_template, url_for, request, redirect, g, jsonify
from dotenv import load_dotenv
import os
from os.path import exists
import re
import requests
from sqlalchemy.sql import text, func
from models import db, Merchandise
from reset_db import reset_database

load_dotenv()

app = Flask(__name__)

PRINTFUL_API_KEY = os.getenv("PRINTFUL_API_KEY")
PRINTFUL_API_BASE = "https://api.printful.com"

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# File Saving Path
MERCH_FOLDER = os.path.join(app.root_path, 'static', 'merchpics')
PHOTO_EXTENSIONS = {'png', 'jpg', 'webp'}

app.config['MERCH_FOLDER'] = MERCH_FOLDER

# app.config.from_pyfile(app.root_path + '/config_defaults.py')
# if exists(app.root_path + '/config.py'):
#     app.config.from_pyfile(app.root_path + '/config.py')

# INDEX
@app.route("/", methods=['GET','POST'])
def index():
    featured = Merchandise.query.filter(Merchandise.featured==True).order_by(Merchandise.date_created.desc()).all()
    return render_template('index.html', featured=featured)

# SHOPPING
@app.route("/shop")
def shop():
    merch = Merchandise.query.order_by(Merchandise.name).all()
    return render_template("shop.html", merch=merch)

@app.route("/shop/<int:item_id>")
# make dynamic url later
def item(item_id=None):
    if item_id:
        item_info = Merchandise.query.filter(Merchandise.id==item_id).first()
        return render_template('item.html', item_info=item_info)
    else:
        merch = Merchandise.query.order_by(Merchandise.name).all()
        return render_template("shop.html", merch=merch)


# ADMIN
@app.route("/login", methods=['POST'])
def login():
    pass

with app.app_context():
    db.drop_all()
    db.create_all()
    reset_database()

if __name__ == "__main__":
    app.run(debug=True)