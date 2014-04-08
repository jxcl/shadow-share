from flask import g
import gnupg

import base64

from server import app, enig_db

def get_db():
    if not hasattr(g, "enig_db"):
        g.enig_db = enig_db.EnigDB(app.config)

    return g.enig_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, "enig_db"):
        g.enig_db.close()

def file_record(user_name, original_file_name, target_user=None):
    db = get_db()

    record = db.get_file_record(user_name)

    if record is None:
        db.create_file_record(user_name, target_user, original_file_name)
    else:
        db.update_file_record(user_name, target_user, original_file_name)

def open_and_encode_file(user_name, file_path):
    db = get_db()
    file_name = db.get_file_name(user_name)

    with open(file_path, "rb") as fp:
        bts = fp.read()
        b64_bytes = base64.b64encode(bts).decode("utf-8")
        response = {
            "status": "SUCCESS",
            "file_name": file_name,
            "data": b64_bytes
            }
    return response

def key_valid(key_data):
    gpg = gnupg.GPG(gnupghome="gnupg")
    import_result = gpg.import_keys(key_data)

    if import_result.count == 1:
        gpg.delete_keys(import_result.fingerprints[0])
        return True
    else:
        return False

