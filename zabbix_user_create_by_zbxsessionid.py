#!/usr/bin/env python3
"""
Usage: zabbix_user_create_by_zbxsessionid.py --api http://IP/zabbix/api_jsonrpc.php --zbx-sessionid <id> --user newuser --password newpass
"""
import argparse
import json

import requests
from pyzabbix import ZabbixAPI


#api_address="http://192.168.56.102/zabbix/api_jsonrpc.php"
parser = argparse.ArgumentParser(description="Create a Zabbix user with a provided session id.")
parser.add_argument("--api", required=True, help="Zabbix API URL, e.g. http://IP/zabbix/api_jsonrpc.php")
parser.add_argument("--zbx-sessionid", required=True, help="Zabbix session id")
parser.add_argument("--user", required=True, help="New username")
parser.add_argument("--password", required=True, help="New user password")
args = parser.parse_args()

api_address = args.api
zbx_sessionid = args.zbx_sessionid
user = args.user
password = args.password

url = api_address
headers = {'Content-type': 'application/json'}
data = {
    "jsonrpc": "2.0",
    "method": "user.create",
    "params": {
        "alias": user,
        "passwd": password,
        "type": "3",
        "usrgrps": [{"usrgrpid": "7"}],
    },
    "auth": zbx_sessionid,
    "id": 1,
}
answer = requests.post(url, data=json.dumps(data), headers=headers)
print(answer)
response = answer.json()
print(response)
print("testing user parameters:")
zapi = ZabbixAPI(api_address)
zapi.login(user, password)
print("Connected to Zabbix API Version %s" % zapi.api_version())
# data = {"jsonrpc": "2.0", "method": "user.login", "params": {
#     "user": user, "passwd": password },
#         "auth": None,
#         "id": 1
#         }
# answer = requests.post(url, data=json.dumps(data), headers=headers)
# print(answer)
# response = answer.json()
# print(response)
