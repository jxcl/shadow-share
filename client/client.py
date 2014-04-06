import json
import requests
import argparse
import base64
import gnupg
import re

def store(user_name, file_name):
    url = 'http://localhost:5000/{}/store/'.format(user_name)
    p = re.compile('^(.+) <.*$')

    with open(file_name, "rb") as fp:
        bts = fp.read()
        g = gnupg.GPG(gnupghome='gnupg')
        public_keys = g.list_keys()
        for key in public_keys:
            s = p.match(key['uids'][0]).group(1)
            if s == user_name:
                # encrypt with gpg and sign with private key
                encrypted_data = g.encrypt(bts, 
                                                 key['fingerprint'],
                                                 sign=g.list_keys(True)[0]['fingerprint'],
                                                 armor=False
                                                 )
                print(encrypted_data.data)
                b64_bytes = base64.b64encode(encrypted_data.data).decode('utf-8')
                payload = {
                    "file_name": file_name,
                    "file_data": b64_bytes
                    }

    headers = {'content-type': 'application/json'}
    r = requests.post(url,data=json.dumps(payload), headers=headers)

def retrieve(user_name):
    url = 'http://localhost:5000/{}/store/'.format(user_name)
    r = requests.get(url)
    req_obj = r.json()
    if req_obj['status'] == 'SUCCESS':
        print('Successfully Retrieved')
        g = gnupg.GPG(gnupghome='gnupg')
        encrypted_file_data = base64.b64decode(req_obj["file_data"])
        decrypted_data = g.dcrypt(encrypted_file_data)
        print(decrypted_data)
        # verify that data was signed
        file_name = req_obj["file_name"]

        with open(file_name,"wb") as fp:
            fp.write(file_data)
    else:
        print('Failed: {}'.format(obj_req['error_message']))

def register(user_name):
    url = 'http://localhost:5000/{}/register/'.format(user_name)
    g = gnupg.GPG(gnupghome='gnupg')
    input_data = g.gen_key_input(
        key_type="RSA",
        key_length = 512,
        name_real = user_name
        )

    armoured_pub_key =g.export_keys('B0402C72CCDDF8A2')
    payload = {
        "user_name" : user_name,
        "public_key" : armoured_pub_key
        }
    headers = {'content-type': 'application/json'}
    r = requests.post(url,data=json.dumps(payload), headers=headers)
    print(r.json())

def get_key(user_name):
    url = 'http://localhost:5000/{}/register/'.format(user_name)
    r = requests.get(url)
    req_obj = r.json()
    if req_obj['status'] == 'SUCCESS':
        print('Get_Key Succeeded')
        g = gnupg.GPG(gnupghome='gnupg')
        g.import_keys(req_obj['public_key'])
    else:
        print('Failed: {}'.format(req_obj['error_message']))

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest='command')

parser_store = subparsers.add_parser('store')
parser_store.add_argument('user_name')
parser_store.add_argument('file_name')

parser_retrieve = subparsers.add_parser('retrieve')
parser_retrieve.add_argument('user_name')

parser_register = subparsers.add_parser('register')
parser_register.add_argument('user_name')

parser_get_key = subparsers.add_parser('get_key')
parser_get_key.add_argument('user_name')
args = parser.parse_args()

if args.command == "store":
    store(args.user_name, args.file_name)
elif args.command == "recieve":
    recieve(args.user_name)
elif args.command == "register":
    register(args.user_name)
elif args.command == "get_key":
    get_key(args.user_name)
