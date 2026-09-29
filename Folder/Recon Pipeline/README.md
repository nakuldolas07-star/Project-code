# Recon Pipeline — README

`./recon.sh target.com` runs a full passive-to-active recon chain and writes
everything to `recon_target.com/`. Only run this against targets you're
explicitly authorized to test (in-scope for a bug bounty program, or a
system you own/have written permission to assess).

## Requirements

Install on Kali:
```
sudo apt install seclists nmap wafw00f hydra
go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install github.com/projectdiscovery/dnsx/cmd/dnsx@latest
go install github.com/projectdiscovery/httpx/cmd/httpx@latest
go install github.com/projectdiscovery/naabu/v2/cmd/naabu@latest
go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
go install github.com/projectdiscovery/katana/cmd/katana@latest
go install github.com/epi052/feroxbuster@latest   # or apt install feroxbuster
sudo apt install amass
```
Update nuclei templates once: `nuclei -update-templates`

Override the wordlist or thread count at runtime:
```
WORDLIST=/path/to/list.txt THREADS=100 ./recon.sh target.com
```

## What each stage does

**subfinder + amass — subdomain enumeration**
Both are passive subdomain discovery tools pulling from certificate
transparency logs, DNS databases, and other public sources. Running both
and merging (`unique_subdomains.txt`) covers more ground than either alone,
since their data sources don't fully overlap.

**dnsx — DNS resolution**
Takes the raw subdomain list and confirms which actually resolve (A/AAAA/CNAME
records), filtering out dead or unregistered names before you spend time
scanning them. Output: `resolved_dns.txt`, `resolved_hosts.txt`.

**httpx — HTTP probing**
Checks which resolved hosts are actually serving HTTP/HTTPS, and grabs
status codes, page titles, and detected technologies (`live_web_servers.txt`).
This is your target list for every web-layer tool downstream.

**naabu — fast port scanning**
A fast SYN-based port scanner used to sweep all resolved hosts across the
top 1000 ports quickly. It's a triage step, not a deep scan.

**nmap — service/version detection**
Run only against hosts naabu found open ports on, with `-sV` to identify
what's actually running on each port (software + version). This is slower
and more accurate than naabu, which is why it's a second pass rather than
the primary scanner.

**wafw00f — WAF fingerprinting**
Identifies whether a web application firewall is in front of a target and
which one. Useful for knowing whether nuclei/feroxbuster results might be
getting filtered or rate-limited by a WAF rather than reflecting the real
app.

**katana — crawling**
Crawls each live site to pull out URLs, JS files, and endpoints (including
ones referenced in JavaScript via `-jc`). This surfaces attack surface that
directory brute-forcing alone won't find (API routes, parameters, etc.).

**feroxbuster — content/directory discovery**
Brute-forces directories and files on each live web server using a SecLists
wordlist, to find unlinked admin panels, backup files, and hidden paths.

**nuclei — vulnerability scanning**
Runs community-maintained templates against all live URLs to flag known
CVEs, misconfigurations, exposed panels, default credentials pages, etc.
Filtered here to low/medium/high/critical severity.

## hydra — NOT automated, run manually

Hydra brute-forces login credentials against a specific service (SSH, FTP,
a web login form, etc.). It's deliberately left out of the automated chain
because:

- It actively attempts authentication, which is a different risk category
  than passive/read-only recon — many bug bounty programs explicitly
  restrict or forbid brute-forcing.
- Running it blindly against every discovered login page (rather than one
  you've reviewed) is a fast way to trigger account lockouts, WAF bans, or
  scope violations.

If a program's scope explicitly permits credential testing and you've
identified a specific login form worth testing, run it by hand, e.g.:

```
# HTTP form login
hydra -L users.txt -P /usr/share/seclists/Passwords/Common-Credentials/10-million-password-list-top-1000.txt \
  target.com http-post-form "/login:user=^USER^&pass=^PASS^:F=incorrect"

# SSH
hydra -L users.txt -P passwords.txt ssh://target.com
```

Always confirm the exact login endpoint, parameter names, and failure
string manually first (e.g. via browser dev tools) rather than guessing —
and check the program's rules of engagement for rate limits or an outright
ban on brute-force testing before running this.

## Output files

| File | Contents |
|---|---|
| `unique_subdomains.txt` | All discovered subdomains |
| `resolved_hosts.txt` | Subdomains that resolve via DNS |
| `live_web_servers.txt` / `live_urls.txt` | Live HTTP(S) services |
| `open_ports.txt` | naabu fast port sweep |
| `nmap_services.txt` | Service/version detail on open ports |
| `waf_results.txt` | WAF detection per site |
| `katana_urls.txt` | Crawled URLs/endpoints |
| `ferox_*.txt` | Directory brute-force results per site |
| `vulnerabilities.txt` | nuclei findings |
