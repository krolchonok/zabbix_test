#!/usr/bin/env python3
"""
Usage: zabbix_host_scan_by_pyzabbix.py --api http://IP/zabbix/api_jsonrpc.php --user Admin --password zabbix
"""
import argparse

from pyzabbix import ZabbixAPI

parser = argparse.ArgumentParser(description="List Zabbix hosts via API.")
parser.add_argument("--api", required=True, help="Zabbix API URL, e.g. http://IP/zabbix/api_jsonrpc.php")
parser.add_argument("--user", required=True, help="Zabbix username")
parser.add_argument("--password", required=True, help="Zabbix password")
args = parser.parse_args()

api_address = args.api
user = args.user
password = args.password

zapi = ZabbixAPI(api_address)
zapi.login(user, password)
print("Connected to Zabbix API Version %s" % zapi.api_version())

for h in zapi.host.get(output="extend"):
    hostid = h["hostid"]
    host = h["host"]
    print("found host: ", host, "hostid: ", hostid)
