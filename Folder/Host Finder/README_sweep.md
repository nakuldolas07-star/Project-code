# Ping Sweep / Host Discovery

A small Python script that pings every address in a network and shows which hosts are alive. It also tries to look up the hostname of each live host. It uses only the standard library, so there is nothing to install.

## Requirements

- Python 3.6 or newer
- The `ping` command on your system (Windows, Linux and macOS all have it)

## How to use

```
python sweep.py 192.168.1.0/24
```

The argument is the network in CIDR form.

Examples:

```
python sweep.py 192.168.1.0/24
python sweep.py 10.0.0.0/24
python sweep.py 127.0.0.1/32
```

`/24` means 254 hosts (x.x.x.1 to x.x.x.254). A smaller number like `/16` means a lot more hosts and will take much longer.

## Example output

```
sweeping 192.168.1.0/24 ...
[+] 192.168.1.1 is up    router.local
[+] 192.168.1.14 is up    laptop.local
[+] 192.168.1.20 is up
done, 3 hosts up
```

## How it works

1. It turns the network into a list of host addresses.
2. It sends one ping to each address, 100 at a time.
3. If the ping is answered, the host is counted as up.
4. It tries a reverse DNS lookup to get the hostname.
5. It prints the live hosts in order at the end.

## Notes

- Some devices block ping (many firewalls do), so they will not show up even if they are on. This scan only finds hosts that answer ping.
- The hostname column is empty when the network has no name for that address. That is normal.
- On Windows, a router saying "destination unreachable" can sometimes look like a reply, so you may see a false host now and then.

## Legal

Only scan networks you own or have permission to test. Your home network is a good place to practice.
