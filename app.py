from flask import Flask, render_template, url_for, request, redirect, g
from os.path import exists
import re

app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True

# app.config.from_pyfile(app.root_path + '/config_defaults.py')
# if exists(app.root_path + '/config.py'):
#     app.config.from_pyfile(app.root_path + '/config.py')

import database, testdb

@app.route("/")
def index():
    featured = database.get_featured()
    print(featured)
    return render_template('index.html', featured=featured)

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == "__main__":
    app.run(debug=True)