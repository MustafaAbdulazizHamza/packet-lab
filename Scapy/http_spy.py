import scapy.all as scapy
from scapy.layers import http
import sys, colorama
def Sniffer(Interface):
    scapy.sniff(iface=Interface, store=False, prn=Process)
def Process(Packet): 
        if Packet.haslayer(http.HTTPRequest):
            print(colorama.Fore.WHITE+ "[* {}{} *]".format(Packet[http.HTTPRequest].Host.decode(), Packet[http.HTTPRequest].Path.decode()))
            if Packet.haslayer(scapy.Raw):
                print(colorama.Fore.GREEN+f"\n****\n[{Packet[scapy.Raw].load.decode()}]\n****\n")
while True:
    try:
        iface = input(colorama.Fore.YELLOW+"Enter the Network Adapter you want to capture(Enter q to quit)\n>")
        if iface == 'q':
             sys.exit(1)
        Sniffer(iface)
    except Exception as e:
        print(colorama.Fore.RED+f"* {e}*")
