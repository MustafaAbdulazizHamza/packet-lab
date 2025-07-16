from scapy.all import rdpcap
from sys import argv, exit
import os
import logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
if len(argv) < 3:
    print(f"Usage:\n\tpython3 {argv[0]} <pcap file> <IP address>")
    quit()
if not os.path.isfile(argv[1]):
    logging.error(f"The file {argv[1]} was not found!")
    exit(404)
pkts = rdpcap(argv[1])
for pkt in pkts:
    if pkt["IP"].src == argv[2]:
        logging.info(f"Found MAC address {pkt['Ether'].src} corresponding to IP address {argv[2]}")
        exit(0)
logging.info(f"No packet found with source IP {argv[2]}.")
