
# Cerberus
Cerberus is a Golang-based port scanner designed to detect a running Pandora server during the reconnaissance phase. The tool performs a full TCP scan, followed by an HTTPS probe to check for the presence of a valid https://IP:Port/secret endpoint. If such an endpoint is discovered, it confirms that Pandora is running on the associated port.
## Usage  

```bash
./Cerberus [options]

Options

-p string

Specifies the port(s) to scan, separated by commas.

-t string
Specifies the target IP address or hostname.

-v
Enables Pandora-specific scanning mode.
