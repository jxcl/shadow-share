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
        req_obj = request.get_json()

        file_data = base64.b64decode(req_obj["file_data"])
        file_name = req_obj["file_name"]
        file_path = path.join(app.config['UPLOAD_FOLDER'],
                              "{}.stor".format(user_name))

        with open(file_path, "wb") as fp:
            fp.write(file_data)

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
            "filename": "dummy_filename",
            "data": b64_bytes
            }

        return json.jsonify(response)


