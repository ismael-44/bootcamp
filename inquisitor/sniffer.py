from scapy.all import *
import logging

def packet_handler(packet):
    if packet.haslayer(Raw):
        raw_data = packet[Raw].load.decode("utf-8", errors="ignore")
        if "USER" in raw_data:
            logging.warning("User found: %s", raw_data)
        
        if "PASS" in raw_data:
            logging.warning("Password found: %s", raw_data)
        
        if packet.haslayer(TCP):
            src_port = packet[TCP].sport
            dst_port = packet[TCP].dport

            # Verificar si es un comando RETR o STOR en FTP
            if dst_port == 21 and "RETR" in raw_data:
                command_parts = raw_data.strip().split()
                filename = command_parts[1]
                logging.warning("File attempted to download: %s", filename)
                                   
            if dst_port == 21 and "STOR" in raw_data:
                command_parts = raw_data.strip().split()
                filename = command_parts[1]
                logging.warning("File attempted to upload: %s", filename)

# Configurar el registro de eventos
logging.basicConfig(filename='traza.log', level=logging.WARNING)

# Filtrar paquetes en tiempo real
print("Sniffing packets...")
sniff(prn=packet_handler, filter="tcp")