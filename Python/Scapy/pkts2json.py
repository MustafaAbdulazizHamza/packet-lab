import json
from scapy.all import Packet, rdpcap
from scapy.packet import Raw
from sys import argv, exit
import os
"""
This script converts packets from a capture file (PCAP) into a descriptive JSON format.

You can use this script by providing the input PCAP file and the output directory.
"""

def serialize_value(value):
    try:
        if hasattr(value, "showname"):
            return str(value)
        if isinstance(value, bytes):
            return value.hex()
        if isinstance(value, Raw):
            return value.load.hex()
        json.dumps(value)
        return value
    except (TypeError, OverflowError):
        return str(value)

def scapy_packet_to_json(pkt: Packet) -> str:
    layers = {}
    current_layer = pkt
    while current_layer:
        layer_name = current_layer.__class__.__name__
        fields = {}
        for field in current_layer.fields_desc:
            value = current_layer.getfieldval(field.name)
            fields[field.name] = serialize_value(value)
        layers[layer_name] = fields
        current_layer = current_layer.payload if current_layer.payload else None
    return json.dumps(layers, separators=(',', ':'))

if len(argv) != 3:
    print("Usage:\n\tpython3 {} <PCAP file> <Output Directory>".format(argv[0]))
    exit(1)
if not os.path.isfile(argv[1]):
    print("The file named {} was NOT found!".format(argv[1]))
    exit(404)
if not os.path.isdir(argv[2]): os.makedirs(argv[2])
pkts = rdpcap(argv[1])
for i, pkt in enumerate(pkts):
    jsn = scapy_packet_to_json(pkt)
    with open(os.path.join(argv[2], f"pkt_{i}.json"), "w") as jsf:
        jsf.write(jsn) 