from flask import Flask, request, json, g
from os import path
import base64

import server.enig_db

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['DB_PATH'] = 'server/enigshare.db'
app.debug = True

def get_db():
    if not hasattr(g, "enig_db"):
        g.enig_db = enig_db.EnigDB(app.config)

    return g.enig_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, "enig_db"):
        g.enig_db.close()

@app.route("/<user_name>/register_key/")
def register(user_name):
    if request.method == 'POST':
        req_qb = request.get_json()

@app.route("/<user_name>/store/", methods=["POST"])
def store(user_name):
    if request.method == 'POST':
        req_obj = request.get_json()

        file_data = base64.b64decode(req_obj["file_data"])
        file_name = req_obj["file_name"]
        file_path = path.join(app.config['UPLOAD_FOLDER'],
                              "{}.stor".format(user_name))
        file_target_user = req_object["file_target_user"]

        with open(file_path, "wb") as fp:
            fp.write(file_data)

        return json.jsonify({"message": "SUCCESS"})

def open_and_encode_file(file_path):
    with open(file_path, "rb") as fp:
        bts = fp.read()
        b64_bytes = base64.b64encode(bts).decode("utf-8")
        response = {
            "message": "SUCCESS",
            "filename": "dummy_filename",
            "data": b64_bytes
            }
    return response

@app.route("/<user_name>/retrieve/")
def retrieve(user_name):
    file_path = path.join(app.config['UPLOAD_FOLDER'],
                          "{}.gpg".format(user_name))
    db = get_db()
    if db.user_exists(user_name):
        if path.exists(file_path):
            response = open_and_encode_file(file_path)
            return json.jsonify(response)
        else:
            response = {
                "message": "FAIL",
                "error": "User does not have a file stored."
               }
            return json.jsonify(response)
    else:
        response = {
            "message": "FAIL",
            "error": "User does not exist"
            }
        return json.jsonify(response)
