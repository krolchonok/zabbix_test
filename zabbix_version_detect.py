#!/usr/bin/env python3
"""
Usage: zabbix_version_detect.py --zab-page http://IP/zabbix/index.php
Detects Zabbix version by the docs link on the login page.
"""
import argparse
import re
import urllib.request

from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(description="Detect Zabbix version from login page docs link.")
parser.add_argument("--zab-page", required=True, help="Zabbix login page URL, e.g. http://IP/zabbix/index.php")
args = parser.parse_args()

zab_page = args.zab_page
page = urllib.request.urlopen(zab_page)
soup = BeautifulSoup(page, 'html.parser')
for link in soup.find_all('a', attrs={'href': re.compile("documentation")}):
    version = link.get('href')

parts = re.split('/', version)

a = ''.join(parts[4:5])
print("zabbix version is", a)
