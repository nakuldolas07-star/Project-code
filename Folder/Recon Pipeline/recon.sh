#!/bin/bash
set -euo pipefail

TARGET="${1:?Usage: $0 <target-domain>}"
OUTPUT_DIR="recon_$TARGET"
WORDLIST="${WORDLIST:-/usr/share/seclists/Discovery/Web-Content/raft-medium-directories.txt}"
THREADS="${THREADS:-50}"

REQUIRED_TOOLS=(subfinder dnsx amass httpx nmap naabu feroxbuster wafw00f nuclei katana)
for tool in "${REQUIRED_TOOLS[@]}"; do
    command -v "$tool" >/dev/null 2>&1 || { echo "[!] Missing tool: $tool"; exit 1; }
done
[[ -f "$WORDLIST" ]] || { echo "[!] Wordlist not found: $WORDLIST (install seclists)"; exit 1; }

mkdir -p "$OUTPUT_DIR"
cd "$OUTPUT_DIR"

# 1. Subdomain enumeration
echo "[+] Subdomain enumeration"
subfinder -d "$TARGET" -all -silent -o subfinder_raw.txt
amass enum -passive -d "$TARGET" -o amass_raw.txt
cat subfinder_raw.txt amass_raw.txt | sort -u > unique_subdomains.txt
echo "[*] $(wc -l < unique_subdomains.txt) unique subdomains"

# 2. DNS resolution + record enrichment
echo "[+] DNS resolution"
dnsx -l unique_subdomains.txt -silent -a -aaaa -cname -resp -o resolved_dns.txt
cut -d' ' -f1 resolved_dns.txt | sort -u > resolved_hosts.txt
echo "[*] $(wc -l < resolved_hosts.txt) resolved hosts"

# 3. HTTP probing
echo "[+] HTTP probing"
httpx -l resolved_hosts.txt -silent -status-code -title -tech-detect -o live_web_servers.txt
cut -d' ' -f1 live_web_servers.txt | sort -u > live_urls.txt
echo "[*] $(wc -l < live_urls.txt) live web services"

# 4. Port scanning (fast sweep, then service/version detail on hits)
echo "[+] Port scanning"
naabu -l resolved_hosts.txt -top-ports 1000 -silent -o open_ports.txt
awk -F: '{print $1}' open_ports.txt | sort -u > hosts_with_open_ports.txt
nmap -sV -iL hosts_with_open_ports.txt -oN nmap_services.txt

# 5. WAF fingerprinting
echo "[+] WAF detection"
wafw00f -i live_urls.txt -o waf_results.txt

# 6. Crawling for endpoints/params
echo "[+] Crawling with katana"
katana -list live_urls.txt -silent -jc -o katana_urls.txt

# 7. Content/directory discovery
echo "[+] Content discovery (feroxbuster)"
while read -r url; do
    feroxbuster -u "$url" -w "$WORDLIST" -t "$THREADS" -q -o "ferox_$(echo "$url" | sed 's|[/:]|_|g').txt" || true
done < live_urls.txt

# 8. Vulnerability scanning
echo "[+] Vulnerability scanning (nuclei)"
nuclei -l live_urls.txt -severity low,medium,high,critical -o vulnerabilities.txt

echo "[+] Recon complete. Results in $OUTPUT_DIR/"
echo "[i] Login brute-forcing is NOT automated. To test a specific discovered"
echo "    login form manually with hydra, see README.md."
