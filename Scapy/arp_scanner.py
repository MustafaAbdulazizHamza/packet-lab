from scapy.all import ARP, Ether, srp
import ipaddress
from rich.table import Table
from rich.console import Console
from rich.panel import Panel
import asyncio
from sys import argv, exit
console = Console()

def print_scan_results(hosts: list[dict[str, str]]) -> None:
    table = Table(title="Scan Results - Found Hosts", show_lines=True)
    table.add_column("MAC Address", style="cyan", no_wrap=True)
    table.add_column("IP Address", style="magenta")
    if not hosts:
        console.print(Panel.fit("[bold red]No Active Host Found[/bold red]"))
        exit(0)
    for host in hosts:
        for mac, ip in host.items():
            table.add_row(mac, ip)

    console.print(table)
class ARP_Scanner:
    def __init__(self, network) -> None:
        self._network = network
    def _ls(self) -> list[str]:
        network = ipaddress.IPv4Network(f"{self._network}", strict=False)
        return [str(ip) for ip in network.hosts()]
    async def __is_active(self, ip: str) -> dict[str, str] | None:
        def send_arp():
            arp = ARP(pdst=ip)
            ether = Ether(dst='ff:ff:ff:ff:ff:ff')
            result = srp(ether / arp, timeout=1, verbose=False)[0]
            for _, rcv in result:
                return {rcv.hwsrc: rcv.psrc}
            return None

        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, send_arp)

    async def Scan(self) -> list[dict[str:str]]:
        ips = self._ls()
        hosts = await asyncio.gather(*(self.__is_active(ip) for ip in ips))
        found_hosts = [host for host in hosts if host]
        return found_hosts
output_temp = """
# Scan Results - Found Hosts
{}
"""

if __name__ == "__main__":
    if len(argv) != 2 or len(argv[1].split("/")) != 2:
        print(f"Usage:\n\tpython3 {argv[0]} <Network ID>/Subnet Mask")
        exit(404)
    scanner = ARP_Scanner(argv[1])
    hosts = asyncio.run(scanner.Scan())
    print_scan_results(hosts)
