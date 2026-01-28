from flask import Flask, render_template, url_for, request, redirect, g, jsonify
from flask_caching import Cache
from dotenv import load_dotenv
import os
from os.path import exists
import re
import requests

config = {
    "DEBUG": True,
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 300
}

load_dotenv()

app = Flask(__name__)

app.config.from_mapping(config)
cache = Cache(app)

PRINTFUL_API_KEY = os.getenv("PRINTFUL_API_KEY")
PRINTFUL_API_BASE = "https://api.printful.com"

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
# @cache.cached(timeout=50)
def index():
    data2 = priv_catalog()
    return render_template('index.html', merch=data2)


if __name__ == "__main__":
    app.run()