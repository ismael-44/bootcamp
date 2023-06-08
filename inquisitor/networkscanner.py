import scapy.all as scapy
import argparse
from colorama import init,Fore

init()
red=Fore.RED
green=Fore.RED
magenta=Fore.MAGENTA

def scan(range):
    arp = scapy.ARP(pdst="172.18.0.1/24")
    broadcast_mac = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_broadcast = broadcast_mac/arp
    answer = scapy.srp(arp_broadcast,timeout=1,verbose=False)[0]
    for client in answer:
        print (f"{red}IP\t\t\tMAC address")
        print (f"{magenta}--"*20)
        print (f"{green}{client[1].psrc}\t\t{client[1].hwsrc}")

def options():
    options = argparse.ArgumentParser()
    options.add_argument("-r","--range",dest="range",help="Network Range Eg: 172.18.0.1/24")
    return options.parse_args()

option=options()
if not option.range:
    print (''' usage: network_scanner.py [-h] [-r RANGE]

options:
  -h, --help            show this help message and exit
  -r RANGE, --range RANGE
                        Network Range Eg: 172.18.0.0/24''')


if option.range:
    scan(option.range)


