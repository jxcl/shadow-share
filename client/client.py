import json
import requests
import base64
import gnupg
import re

def get_our_key_info(gpg, regexp):
    private_keys = gpg.list_keys(True)
    our_key = private_keys[0]
    our_uid = our_key['uids'][0]
    our_user_name = regexp.match(our_uid).group(1)
    our_fingerprint = our_key['fingerprint']
    return (our_user_name, our_fingerprint)

def check_key(regexp, key_list, user_name):
    for key in key_list:
        s = regexp.match(key['uids'][0]).group(1)
        if s == user_name:
            found_key = True
            return key
    return None
    

def auto_key(gpg, regexp, user_name):
    found_key = False
    public_keys = gpg.list_keys()
    key = check_key(regexp, public_keys, user_name)
    # encrypt with gpg and sign with private key
    if key is None:
        key = get_key(user_name)
    return key

def store(user_name, file_name):

    p = re.compile('^(.+) <.*$')
    g = gnupg.GPG(gnupghome='gnupg')
    our_user_name, our_fingerprint = get_our_key_info(g, p)
    print(our_user_name)
    url = 'http://localhost:5000/{}/store/'.format(our_user_name)
    with open(file_name, "rb") as fp:
        bts = fp.read()
        key = auto_key(g, p, user_name)
        if key is None:
            print('User Not Found')
            return
        encrypted_data = g.encrypt(bts,
                                   key['fingerprint'],
                                   sign=our_fingerprint,
                                   armor=False,
                                   #DO NOT FUCKING LEAVE THIS HERE
                                   always_trust=True
                                   )
        b64_bytes = base64.b64encode(encrypted_data.data).decode('utf-8')
        payload = {
            "file_name": file_name,
            "file_data": b64_bytes,
            "file_target_user": user_name
            }    
        headers = {'content-type': 'application/json'}
        r = requests.post(url,data=json.dumps(payload), headers=headers)
    
        
def retrieve(user_name):
    url = 'http://localhost:5000/{}/retrieve/'.format(user_name)
    r = requests.get(url)
    req_obj = r.json()
    if req_obj['status'] == 'SUCCESS':
        print('Successfully Retrieved')
        g = gnupg.GPG(gnupghome='gnupg')
        encrypted_file_data = base64.b64decode(req_obj["data"])
        decrypted_data = g.decrypt(encrypted_file_data)
        print(decrypted_data)
        # verify that data was signed
        if decrypted_data.signature_id is not None:
            print('Signature Verified with Trust: ',decrypted_data.trust_text)
            file_name = req_obj["file_name"]
            with open(file_name,"wb") as fp:
                fp.write(decrypted_data.data)
        else:
            print('Signature Verification Failed')
        
    else:
        print('Failed: {}'.format(obj_req['error_message']))

def get_private_keyid(gpg):
    return gpg.list_keys(True)[0]['keyid']

def register(user_name):
    url = 'http://localhost:5000/{}/register/'.format(user_name)
    g = gnupg.GPG(gnupghome='gnupg')
    input_data = g.gen_key_input(
        key_type="RSA",
        key_length = 512,
        name_real = user_name
        )
    armoured_pub_key = g.export_keys(get_private_keyid(g))
    payload = {
        "user_name" : user_name,
        "public_key" : armoured_pub_key
        }
    print(armoured_pub_key)
    headers = {'content-type': 'application/json'}
    r = requests.post(url,data=json.dumps(payload), headers=headers)
    print(r.json())

def get_key(user_name):
    url = 'http://localhost:5000/{}/get_key/'.format(user_name)
    r = requests.get(url)
    req_obj = r.json()
    if req_obj['status'] == 'SUCCESS':
        print('Get_Key Succeeded')
        g = gnupg.GPG(gnupghome='gnupg')
        imported_key = g.import_keys(req_obj['public_key'])
        print(g.list_keys())
        return imported_key
    else:
        print('Failed: {}'.format(req_obj['error_message']))

