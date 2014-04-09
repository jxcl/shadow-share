import json
import requests
import base64
import re
import os.path
import gnupg
from client import ss_config

def check_key(regexp, key_list, user_name):
    for key in key_list:
        s = regexp.match(key['uids'][0]).group(1)
        if s == user_name:
            return key
    return None

def auto_key(gpg, regexp, user_name):
    public_keys = gpg.list_keys()
    key = check_key(regexp, public_keys, user_name)
    # encrypt with gpg and sign with private key
    if key is None:
        get_key(gpg, user_name)
        key = check_key(regexp, gpg.list_keys(), user_name)
    return key

def put(user_config, file_name):
    put_for(user_config, user_config['user_name'], file_name)

def put_for(user_config, user_name, file_name):
    p = re.compile('^(.+) <.*$')
    gpg = gnupg.GPG(gnupghome=user_config['gnupghome'])
    url = 'http://localhost:5000/{}/store/'.format(user_config['user_name'])
    with open(file_name, "rb") as fp:
        bts = fp.read()
        key = auto_key(gpg, p, user_name)
        if key is None:
            print('User Not Found')
            return
        encrypted_data = gpg.encrypt(bts,
                                   key['fingerprint'],
                                   sign=user_config['fingerprint'],
                                   armor=False,
                                   #DO NOT FUCKING LEAVE THIS HERE
                                   always_trust=True
                                   )
        b64_bytes = base64.b64encode(encrypted_data.data).decode('utf-8')
        payload = {
            "file_name": os.path.basename(file_name),
            "file_data": b64_bytes,
            "file_target_user": user_name
            }
        headers = {'content-type': 'application/json'}
        requests.post(url,data=json.dumps(payload), headers=headers)

def get(user_config):
    get_from(user_config['user_name'])

def get_from(user_config, user_name):
    url = 'http://localhost:5000/{}/retrieve/'.format(user_name)
    r = requests.get(url)
    req_obj = r.json()
    if req_obj['status'] == 'SUCCESS':
        get_key(user_name)
        gpg = gnupg.GPG(gnupghome=user_config['gnupghome'])
        encrypted_file_data = base64.b64decode(req_obj["data"])
        decrypted_data = gpg.decrypt(encrypted_file_data)
        # verify that data was signed
        if decrypted_data.signature_id is not None:
            print('Signature verified with ',decrypted_data.trust_text)
            file_name = req_obj["file_name"]
            with open(file_name,"wb") as fp:
                fp.write(decrypted_data.data)
            print('Successfully retrieved file: ', file_name)
        else:
            print('Signature verification failed.')
    else:
        print('Failed: {}'.format(req_obj['error_message']))

def register(user_config, user_name):
    url = 'http://localhost:5000/{}/register/'.format(user_name)
    gpg = gnupg.GPG(gnupghome=user_config['gnupghome'])
    armoured_pub_key = gpg.export_keys(user_config['key_id'])
    payload = {
        "user_name" : user_name,
        "public_key" : armoured_pub_key
        }
    headers = {'content-type': 'application/json'}
    response = requests.post(url,
                             data=json.dumps(payload),
                             headers=headers).json()

    if response['status'] == 'SUCCESS':
        ss_config.add_user_name(user_name)
    else:
        print("Error: ", response['error_message'])

def get_key(gpg, user_name):
    url = 'http://localhost:5000/{}/get_key/'.format(user_name)
    r = requests.get(url)
    req_obj = r.json()
    if req_obj['status'] == 'SUCCESS':
        imported_key = gpg.import_keys(req_obj['public_key'])
        return imported_key
    else:
        print('Failed: {}'.format(req_obj['error_message']))
        return None
