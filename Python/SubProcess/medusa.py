import subprocess
import os
import sys
import json
class Medusa:
    def __init__(self, usernames:str, wordlist:str, module:str, port: int) -> None:
        if not os.path.isfile(usernames):
            print("The usernames file was not found!")
            sys.exit(404)
        if not os.path.isfile(wordlist):
            print("The wordlist file was not found!")
            sys.exit(404)
        self._usernames = usernames
        self._wordlist = wordlist
        self._module = module
        self.port = port
        self.accounts = []
    def Run(self, host:str) -> None:
        p = subprocess.run(f"medusa -h {host} -M {self._module} -U {self._usernames} -P {self._wordlist} -n {self.port}", shell=True, capture_output=True, text=True)
        if p.returncode != 0:
            print(p.stderr)
            sys.exit(1)
        out = [o for o in p.stdout.split("\n") if "[SUCCESS]" in o]
        self.accounts[host] = [(out[i].split()[6], out[i].split()[8]) for i in range(len(out))]
    def As_JSON(self, output: str) -> None:
        with open(output, 'w') as f:
            js = json.dumps(self.accounts,indent=4)
            f.write(js)