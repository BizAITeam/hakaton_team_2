import requests
import json
from pprint import pprint

url = "https://tonai.tech/api/public/v1/services"
headers={"key":"key_tonai_3f26efbb-3f4f-41ab-8abc-824460a947f8"}

response = json.loads(requests.get(url, headers=headers).text)

pprint(response)
# qdfmo6h8dn62wyx           gpt-4 6j99xutxsmiwpt6
'''
    'id':                       'name':
    'z3vvmcbnwdynx2x'           'search'
    'gas59jwbg2sjtrj'           'cv'
'''