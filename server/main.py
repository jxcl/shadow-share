from flask import Flask, request, json
from os import path
import sqlite3
import base64

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.debug = True

@app.route("/<user_name>/store/", methods=["POST"])
def store(user_name):
    if request.method == 'POST':
        f = request.files['file']

        f.save(path.join(app.config['UPLOAD_FOLDER'],
                         "{}.gpg".format(user_name)))
        return json.jsonify({"message": "SUCCESS"})

@app.route("/<user_name>/retrieve/")
def retrieve(user_name):
    file_path = path.join(app.config['UPLOAD_FOLDER'],
                          "{}.gpg".format(user_name))

    with open(file_path, "rb") as fp:
        bts = fp.read()
        b64_bytes = base64.b64encode(bts).decode("utf-8")
        response = {
            "message": "SUCCESS",
            "filename": "dummy_filename"
            "data": b64_bytes
            }

        return json.jsonify(response)


