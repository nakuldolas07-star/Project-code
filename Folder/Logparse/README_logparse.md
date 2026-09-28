# Linux Log Parser

A small Python script that reads a Linux auth log and shows the important stuff: failed logins, the IPs behind them, good logins and sudo commands. It uses only the standard library, so there is nothing to install.

## Requirements

- Python 3.6 or newer
- A Linux auth log file

## How to use

```
python logparse.py /var/log/auth.log
```

With no argument it reads `/var/log/auth.log`. You may need `sudo` to read the file:

```
sudo python3 logparse.py
```

Other log locations:

| System | Auth log file |
|--------|---------------|
| Ubuntu / Debian | `/var/log/auth.log` |
| CentOS / RHEL / Fedora | `/var/log/secure` |

## Example output

```
file: /var/log/auth.log
lines: 5231

== failed logins: 412 ==
   203.0.113.45 - 300
   198.51.100.7 - 112

== usernames they tried ==
   root - 250
   admin - 90
   test - 40

== invalid users ==
   admin - 90
   oracle - 22

== good logins: 3 ==
   Sep 27 09:12:44  bob from 192.168.1.14 (publickey)

== sudo stuff ==
   bob  ran  /usr/bin/apt update - 4 times
```

## What it looks for

- Failed SSH password attempts, counted per IP and per username
- Invalid users (usernames that do not exist on the machine)
- Successful SSH logins, with the time, user, IP and method
- Commands run with sudo

Each section shows the top 5. The good logins section shows the last 5.

## Notes

- A lot of failed logins from one IP usually means someone is guessing passwords (brute force).
- It reads the whole file at once, so a huge log will use more memory.
- It does not read compressed logs like `auth.log.2.gz`. Unzip them first with `gunzip`.

## Legal

Only read logs from machines you own or have permission to check.
