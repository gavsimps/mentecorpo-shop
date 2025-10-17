from flask import Flask, render_template, url_for, request, redirect, g
from os.path import exists
import re

app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True

# app.config.from_pyfile(app.root_path + '/config_defaults.py')
# if exists(app.root_path + '/config.py'):
#     app.config.from_pyfile(app.root_path + '/config.py')

import database, testdb

# INDEX
@app.route("/", methods=['GET','POST'])
def index():
    featured = database.get_featured()
    return render_template('index.html', featured=featured)

# SHOPPING
@app.route("/shop")
def shop():
    merch = database.get_all
    return render_template("shop.html",merch=merch)

@app.route("/shop/<item_id>")
# make dynamic url later
def item(item_id=None):
    if item_id:
        item_info = database.get_item(item_id)
        return render_template('item.html',item_info=item_info)
    else:
        shop_items = database.get_all()
        return render_template('shop.html', shop_items=shop_items)


# ADMIN
@app.route("/login", methods=['POST'])
def login():
    pass

@app.route("/restock")

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == "__main__":
    app.run(debug=True)