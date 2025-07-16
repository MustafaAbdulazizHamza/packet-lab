# Fenrir
Fenrir is a brute-forcing tool designed specifically to target the Pandora service as part of this project. It operates by sending HTTPS requests with credentials sourced from a dictionary. The tool halts either upon successful authentication with valid credentials or after exhausting all entries in the wordlist without success.
## Usage  

```bash
./Fenrir [options]
Options
-p string
Specifies the file path to the password dictionary.

-s int
Defines the port number for the Pandora server.

-t string
Specifies the target host (IP address or domain).

-u string
Provides the file path to the list of usernames.
```
