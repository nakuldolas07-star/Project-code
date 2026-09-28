# Port Scanner

A small Python port scanner. It does a TCP connect scan and tries to grab a banner from each open port. It uses only the standard library, so there is nothing to install.

## Requirements

- Python 3.6 or newer

## How to use

```
python scan.py 127.0.0.1 1 1024
```

The arguments are:

| Argument | Meaning | Default |
|----------|---------|---------|
| target | IP address or hostname | required |
| start | first port to scan | 1 |
| end | last port to scan | 1024 |

More examples:

```
python scan.py 127.0.0.1
python scan.py 127.0.0.1 1 65535
python scan.py scanme.nmap.org 20 100
```

## Example output

```
scanning 127.0.0.1 ports 1 to 1024
[+] 22 open    SSH-2.0-OpenSSH_9.6
[+] 80 open    HTTP/1.0 200 OK
done, 2 open
```

## How it works

1. It tries to connect to every port in the range, 100 at a time.
2. If the connection works, the port is open.
3. It waits for the service to send a banner. Services like SSH and FTP talk first.
4. If nothing arrives, it sends a small HTTP request and reads the reply. This catches web servers.
5. It prints the open ports in order at the end.

## Notes

- Each port waits up to 1 second, so scanning a big range on a remote host can take a while.
- Some ports are open but send no banner, so the banner column will be empty. That is normal.

## Legal

Only scan machines you own or have written permission to test. Scanning other people's systems can be illegal. Safe targets for practice are your own computer (`127.0.0.1`) and `scanme.nmap.org`.
