"""This module contains all http endpoints"""
from flask import request, json

import base64
from os import path

from server import app
from server import io

@app.route("/<user_name>/store/", methods=["POST"])
def store(user_name):
    """Receive a file from a user and store it."""
    if request.method == 'POST':

        req_obj = request.get_json()
        file_data = base64.b64decode(req_obj["file_data"])
        file_name = req_obj["file_name"]
        file_path = path.join(app.config['UPLOAD_FOLDER'],
                              "{}.stor".format(user_name))
        file_target_user = req_obj["file_target_user"]
        io.file_record(user_name, file_name, file_target_user)

        with open(file_path, "wb") as fp:
            fp.write(file_data)

        return json.jsonify({"status": "SUCCESS"})

@app.route("/<user_name>/retrieve/")
def retrieve(user_name):
    """Get a file from local storage and send it to the user."""
    db = io.get_db()
    file_path = path.join(app.config['UPLOAD_FOLDER'],
                          "{}.stor".format(user_name))
    if db.user_exists(user_name):
        if path.exists(file_path):
            response = io.open_and_encode_file(user_name, file_path)
            return json.jsonify(response)
        else:
            response = {
                "status": "FAIL",
                "error_message": "User does not have a file stored."
               }
            return json.jsonify(response)
    else:
        response = {
            "status": "FAIL",
            "error_message": "User does not exist"
            }
        return json.jsonify(response)

@app.route("/<user_name>/register/", methods=["POST"])
def register_key(user_name):
    """Receive a key from the user and index it."""
    db = io.get_db()

    if db.user_exists(user_name):
        response = {
            "status": "FAIL",
            "error_message": "Username already taken."
            }

        return json.jsonify(response)
    else:
        req_obj = request.get_json()
        if "public_key" not in req_obj:
            response = {
                "status": "FAIL",
                "error_message": "You must supply a public key."
                }
            return json.jsonify(response)

        key = req_obj["public_key"]
        if io.key_valid(key):
            db.register_user(user_name, key)
            response = {
                "status": "SUCCESS"
                }
            return json.jsonify(response)
        else:
            response = {
                "status": "FAIL",
                "error_message": "The provided key is not valid."
                }
            return json.jsonify(response)

@app.route("/<user_name>/get_key/")
def get_key(user_name):
    """Send the requested public key to the user."""
    db = io.get_db()

    db_lookup_result = db.user_exists(user_name)

    if not db_lookup_result:
        response = {
            "status": "FAIL",
            "error_message": "No such user exists."
            }
        return json.jsonify(response)

    else:
        response = {
            "status": "SUCCESS",
            "user_name": user_name,
            "public_key": db_lookup_result[1]["public_key"]
            }
        return json.jsonify(response)
