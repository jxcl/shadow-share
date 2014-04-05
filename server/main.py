from flask import Flask, request
from os import path
import sqlite3

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.debug = True

@app.route("/<user_name>/store/", methods=["POST"])
def store(user_name):
    if request.method == 'POST':
        f = request.files['file']
        f.save(path.join(app.config['UPLOAD_FOLDER'],
                         "{}.gpg".format(user_name)))
        return "SUCCESS"

@app.route("/<user_name>/retrieve/")
def retrieve(user_name):

