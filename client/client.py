import json
import requests

def store():
    url = 'http://localhost:5000/will/store'
    files = {'file': ('report.csv', 'some,data,to,send\nanother,row,to,send\n')}
    r = requests.post(url,files=files)
    
store()
