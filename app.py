from flask import Flask, render_template, url_for, request, redirect, g, json, jsonify
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
PRINTFUL_STORE_ID = os.getenv("PRINTFUL_STORE_ID")
PRINTFUL_API_BASE = "https://api.printful.com/"

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

######################################################
#                      PRINTFUL                      #
######################################################
def printful_request(endpoint: str):
    url = f"{PRINTFUL_API_BASE}/{endpoint}"
    response = requests.get(url, headers={
        "Authorization": f"Bearer {PRINTFUL_API_KEY}"
    })
    return response.json()

# CURRENTLY WORKS ACTUALLY 100!!!!!!
@app.route("/products", methods=["GET"])
def get_store_products():
    """Fetch products from your personal Printful store"""
    endpoint = f"store/products"
    data = printful_request(endpoint)
    print(data)
    # products = {
    #     item["id"]: {
    #         "name": item.get("name"),
    #         "thumbnail_url": item.get("thumbnail_url"),
    #         "variants": item.get("variants"),
    #         "synced": item.get("synced"),
    #     }
    #     for item in data.get("result", [])
    # }
    all = jsonify(data)
    print(all)
    return jsonify(data)

def get_catalog():
    endpoint = f"store/products"
    catalog = printful_request(endpoint)["result"]
    
    result = []

    for p in catalog:
        product_id = p["id"]


def priv_catalog():
    endpoint = f"store/products"
    catalog = printful_request(endpoint)["result"]
    
    result = []

    for p in catalog:
        product_id = p["id"]
        detail = printful_request(f"store/products/{product_id}")["result"]
        
        variants = detail["sync_variants"]
        
        result.append({
            "id": p["id"],
            "name": p["name"],
            "thumbnail": p["thumbnail_url"],
            "variants": [
                {
                    "variant_id": v["id"],
                    "name": v["name"],
                    "price": v["retail_price"]
                }
                for v in variants
            ]
        })

    print(result)

    return result


@app.route("/store", methods=["GET"])
def get_store_info():
    data, status = printful_request("stores")
    return jsonify(data), status

@app.route("/order", methods=["POST"])
def create_order():
    """Create a new Printful order"""
    order_data = request.get_json()
    data, status = printful_request("orders", method="POST", data=order_data)
    return jsonify(data), status





##########################################
#              WEBSITE PAGES             #
#########################################

# INDEX
@app.route("/", methods=['GET','POST'])
def index():
    # featured = get_store_products()
    # print(featured)
    featured = Merchandise.query.filter(Merchandise.featured==True).order_by(Merchandise.date_created.desc()).all()
    return render_template('index.html', featured=featured)

# SHOPPING
@app.route("/shop", methods=["GET"])
def shop():
    # url = "https://api.printful.com/store/products"
    # headers = {"Authorization": f"Bearer {PRINTFUL_API_KEY}"}
    # response = requests.get(url, headers=headers)

    # data = response.json()
    # just this one if working
    data2 = priv_catalog()
    # merch = get_store_products()
    # merch = Merchandise.query.order_by(Merchandise.name).all()
    return render_template("shop.html", merch=data2)

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

# with app.app_context():
#     db.drop_all()
#     db.create_all()
#     reset_database()

if __name__ == "__main__":
    app.run(debug=True)