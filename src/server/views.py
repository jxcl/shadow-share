"""This module contains all http endpoints"""
import base64
from flask import request, json, g
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from os import path
from server import app, io, shadowdb

def get_db():
    """Create a database connection and attach it to g"""
    if not hasattr(g, "shadowdb"):
        engine = sqlalchemy.create_engine(app.config['DB_URI'])
        shadowdb.Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        g.session = Session()
        g.shadowdb = shadowdb.ShadowDB(g.session)

    return g.shadowdb

@app.teardown_appcontext
def close_db(error):
    """Tear down db connection."""
    if hasattr(g, "shadowdb"):
        g.session.close()

@app.route("/<user_name>/store/", methods=["POST"])
def store(user_name):
    """Receive a file from a user and store it."""
    if request.method == 'POST':
        db = get_db()
        req_obj = request.get_json()
        file_data = base64.b64decode(req_obj["file_data"])
        file_name = req_obj["file_name"]
        file_path = path.join(app.config['UPLOAD_FOLDER'],
                              "{}.stor".format(user_name))
        file_target_user = req_obj["file_target_user"]
        io.file_record(db, user_name, file_name, file_target_user)

        with open(file_path, "wb") as fp:
            print("Writing data.")
            fp.write(file_data)

        return json.jsonify({"status": "SUCCESS"})

@app.route("/<user_name>/retrieve/")
def retrieve(user_name):
    """Get a file from local storage and send it to the user."""
    db = get_db()
    file_path = path.join(app.config['UPLOAD_FOLDER'],
                          "{}.stor".format(user_name))
    if db.user_lookup(user_name):
        if path.exists(file_path):
            response = io.open_and_encode_file(db, user_name, file_path)
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
            "error_message": "User does not exist."
            }
        return json.jsonify(response)

@app.route("/<user_name>/register/", methods=["POST"])
def register_key(user_name):
    """Receive a key from the user and index it."""
    db = get_db()

    if db.user_lookup(user_name):
        response = {
            "status": "FAIL",
            "error_message": "Username already taken."
            }

        return json.jsonify(response)
    else:
        req_obj = request.get_json()

        if req_obj is None:
            response = {
                "status": "FAIL",
                "error_message": "The json you send could not be parsed."
                }
            return json.jsonify(response)

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
    db = get_db()

    result = db.user_lookup(user_name)

    if not result:
        response = {
            "status": "FAIL",
            "error_message": "No such user exists."
            }
        return json.jsonify(response)

    else:
        response = {
            "status": "SUCCESS",
            "user_name": result.user_name,
            "public_key": result.public_key
            }
        return json.jsonify(response)
