"""ShadowShare server IO module.

This module handles file IO as well as database IO."""
import gnupg
import base64

def file_record(db, user_name, original_file_name, target_user=None):
    """Put a record of the uploaded file name in the database.

    A record includes the user who uploaded it, the original file
    name and the user for whom the file is meant."""

    record = db.get_file_record(user_name)

    if record is None:
        db.create_file_record(user_name, target_user, original_file_name)
    else:
        db.update_file_record(user_name, target_user, original_file_name)

def open_and_encode_file(db, user_name, file_path):
    """Encode a file in base64 so it can be sent over JSON."""
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
    """Check if a GPG key is valid.

    This is done by importing it into our GPG keyring and
    checking the number of keys imported."""

    gpg = gnupg.GPG(gnupghome="gnupg")
    import_result = gpg.import_keys(key_data)

    if import_result.count == 1:
        gpg.delete_keys(import_result.fingerprints[0])
        return True
    else:
        return False

