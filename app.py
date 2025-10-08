from flask import Flask, render_template, url_for, request, redirect
from os.path import exists
import re

app = Flask(__name__)

app.config.from_pyfile(app.root_path + '/config_defaults.py')
if exists(app.root_path + '/config.py'):
    app.config.from_pyfile(app.root_path + '/config.py')

import database

@app.route("/")
def index():
    return render_template('index.html')