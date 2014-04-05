import json
import requests
import argparse
import base64

def store(user_name, file_name):
    url = 'http://localhost:5000/{}/store/'.format(user_name)
    
    with open(file_name, "rb") as fp:
        bts = fp.read()
        b64_bytes = base64.b64encode(bts).decode("utf-8")
        
        payload = {
            "file_name": file_name,
            "file_data": b64_bytes
            }
    
    print("Flag: " + json.dumps(payload))
    headers = {'content-type': 'application/json'}
    r = requests.post(url,data=json.dumps(payload), headers=headers)

def retrieve(user_name):
    url = 'http://localhost:5000/{}/store/'.format(user_name)
    r = requests.get(url)
    req_obj = r.json()
    if req_obj['message'] == 'SUCCESS':
        print('SUCCESSFULLY Retrieved')
        file_data = base64.b64decode(req_obj["file_data"])
        file_name = req_obj["file_name"]
        
        with open(file_name,"wb") as fp:
            fp.write(file_data)
    elif:
        print('Failed')

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest='command')

parser_store = subparsers.add_parser('store')
parser_store.add_argument('user_name')
parser_store.add_argument('file_name')

parser_retrieve = subparsers.add_parser('retrieve')
parser_retrieve.add_argument('user_name')

args = parser.parse_args()
#print(args_p)
if args.command == "store":
    store(args.user_name, args.file_name)
elif args.command == "recieve":
    recieve(args.user_name)

