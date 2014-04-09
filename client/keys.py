from client import ss_config
import json
import requests

def get_key_from_fingerprint(gpg, fingerprint):
    keys = gpg.list_keys()
    for key in keys:
        if key['fingerprint'] == fingerprint:
            return key

    return None

def key_local_lookup(gpg, user_name):
    user_name_map_file = ss_config.CONFIG_DIRECTORY / "maps.json"
    if not user_name_map_file.exists():
        return None

    user_name_dict = json.load(user_name_map_file.open())
    if user_name in user_name_dict:
        user_fingerprint = user_name_dict[user_name]
        return user_fingerprint
    else:
        return None

def store_keyid(key, user_name):
    user_name_map_file = ss_config.CONFIG_DIRECTORY / "maps.json"

    if user_name_map_file.exists():
        user_name_dict = json.load(user_name_map_file.open())
    else:
        user_name_dict = {}
    user_name_dict[user_name] = key.fingerprints[0]
    json.dump(user_name_dict, user_name_map_file.open("w"))
    return key.fingerprints[0]

def key_remote_lookup(gpg, config, user_name):
    url = config['server_url'] + '/{}/get_key/'.format(user_name)
    r = requests.get(url)
    req_obj = r.json()
    if req_obj['status'] == 'SUCCESS':
        imported_key = gpg.import_keys(req_obj['public_key'])
        return store_keyid(imported_key, user_name)
    else:
        print('Failed: {}'.format(req_obj['error_message']))
        exit(1)

def get_key_for_user(gpg, config, user_name):
    fingerprint = key_local_lookup(gpg, user_name)

    if fingerprint is None:
        fingerprint = key_remote_lookup(gpg, config, user_name)

    key = get_key_from_fingerprint(gpg, fingerprint)
    return key
