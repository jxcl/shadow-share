import json
import requests
import argparse

def store(user_name, file_name):
    url = 'http://localhost:5000/{}/store/'.format(user_name)
    files = {'file': open(file_name,'rb')}
    r = requests.post(url,files=files)
    print(r.text)


parse = argparse.ArgumentParser()
parse.add_argument("user_name")
parse.add_argument("file_name")
args = parse.parse_args()
store(args.user_name, args.file_name)
