# Local Network Mapper

A small Python script that maps your local network. It finds the live devices, shows their MAC address and hostname, and checks a few common ports on each one. It uses only the standard library, so there is nothing to install.

## Requirements

- Python 3.6 or newer
- The `ping` and `arp` commands on your system (Windows, Linux and macOS all have them)

## How to use

Let it find your network by itself:

```
python mapper.py
```

Or give it a network:

```
python mapper.py 192.168.1.0/24
```

With no argument it looks at your own IP and scans the `/24` network around it (254 addresses).

## Example output

```
mapping 192.168.1.0/24 ...

IP               MAC                NAME                OPEN PORTS
-----------------------------------------------------------------
192.168.1.1      aa:bb:cc:11:22:33  router.local        53,80,443
192.168.1.14     aa:bb:cc:44:55:66  laptop.local        22  (you)
192.168.1.20     aa:bb:cc:77:88:99  -                   -

done, 3 hosts found
```

## How it works

1. It works out your network from your own IP, or uses the one you typed.
2. It pings every address, 100 at a time.
3. For each host that answers, it looks up the hostname and checks these ports: 21, 22, 23, 53, 80, 139, 443, 445, 3389, 8080.
4. It runs `arp -a` and matches each IP to its MAC address.
5. It prints everything in one table, sorted by IP.

## Notes

- Devices that block ping will not show up.
- The MAC is empty (`-`) for your own machine on some systems, because it is not in your own ARP table.
- A `-` in the name column means the network has no name for that address.
- To change the ports it checks, edit the `ports` list near the top of `mapper.py`.

## Legal

Only scan networks you own or have permission to test. Your home network is a good place to practice.
