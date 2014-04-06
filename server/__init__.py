from flask import Flask, request, json, g
from os import path
import base64
import gnupg

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

def file_record(user_name, target_user=None):
    db = get_db()

    record = db.get_file_record(user_name)

    if record is None:
        db.create_file_record(user_name, target_user)
    else:
        db.update_file_record(user_name, target_user)


@app.route("/<user_name>/store/", methods=["POST"])
def store(user_name):
    if request.method == 'POST':
        db = get_db()
        req_obj = request.get_json()

        file_data = base64.b64decode(req_obj["file_data"])
        file_name = req_obj["file_name"]
        file_path = path.join(app.config['UPLOAD_FOLDER'],
                              "{}.stor".format(user_name))
        file_target_user = req_object["file_target_user"]

        file_record(user_name, file_target_user)

        with open(file_path, "wb") as fp:
            fp.write(file_data)

        return json.jsonify({"status": "SUCCESS"})

def open_and_encode_file(file_path):
    with open(file_path, "rb") as fp:
        bts = fp.read()
        b64_bytes = base64.b64encode(bts).decode("utf-8")
        response = {
            "status": "SUCCESS",
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

def key_valid(key_data):
    gpg = gnupg.GPG(gnupghome="gnupg")
    import_result = gpg.import_keys(key_data)

    if import_result.count == 0:
        gpg.delete_keys(import_result.fingerprints[0])
        return True
    else:
        return False

@app.route("/<user_name>/register/")
def register_key(user_name, methods=["POST"]):

    db = get_db()

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
        if key_valid(key):
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

@app.route("/<user_name>/get_key/")
def get_key(user_name):
    db = get_db()

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
