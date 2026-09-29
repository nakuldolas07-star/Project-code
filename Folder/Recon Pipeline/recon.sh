#!/bin/bash

# Target definition
TARGET=""
OUTPUT_DIR="recon_$TARGET"

echo "=================================================="
echo " Starting Security Pipeline for: $TARGET"
echo " Saving results to directory: /$OUTPUT_DIR"
echo "=================================================="

# Create an organized output directory
mkdir -p "$OUTPUT_DIR"
cd "$OUTPUT_DIR" || exit

# --------------------------------------------------------
# STEP 1: Passive & Active Subdomain Enumeration
# --------------------------------------------------------
echo -e "\n[+] Step 1: Running Subdomain Discovery..."

# Run subfinder
subfinder -d "$TARGET" -o subfinder_raw.txt

# Run amass (using corrected syntax without the undefined -o flag)
amass enum -d "$TARGET" -oTX amass_raw.txt

# Combine, deduplicate, and clean the list
cat subfinder_raw.txt amass_raw.txt | sort -u > unique_subdomains.txt
TOTAL_DOMAINS=$(wc -l < unique_subdomains.txt)
echo "[*] Subdomain discovery complete. Found $TOTAL_DOMAINS unique domains."

# --------------------------------------------------------
# STEP 2: Web Server Probing (Filtering Live Targets)
# --------------------------------------------------------
echo -e "\n[+] Step 2: Probing for live HTTP/HTTPS services..."

# Filter live domains and collect status codes/technologies
httpx-toolkit -l unique_subdomains.txt -silent -o live_web_servers.txt

TOTAL_LIVE=$(wc -l < live_web_servers.txt)
echo "[*] Probing complete. $TOTAL_LIVE endpoints are actively responding."

# --------------------------------------------------------
# STEP 3: Fast Port Scanning
# --------------------------------------------------------
echo -e "\n[+] Step 3: Scanning top infrastructure ports..."

# Use naabu to fast-scan top ports across discovered infrastructure
naabu -l unique_subdomains.txt -top-ports 100 -silent -o open_ports.txt

# --------------------------------------------------------
# STEP 4: Vulnerability Scanning
# --------------------------------------------------------
echo -e "\n[+] Step 4: Launching Nuclei targeting live web servers..."
echo "[*] Scanning for Medium, High, and Critical flaws..."

# Scan the live web stack for security weaknesses and CVEs
nuclei -l live_web_servers.txt -severity medium,high,critical -o vulnerabilities.txt

echo -e "\n=================================================="
echo " Pipeline Finished Successfully!"
echo " Critical files generated:"
echo "  - Unique Domains: $OUTPUT_DIR/unique_subdomains.txt"
echo "  - Active Web Tech: $OUTPUT_DIR/live_web_servers.txt"
echo "  - Open Ports: $OUTPUT_DIR/open_ports.txt"
echo "  - Flaws Found: $OUTPUT_DIR/vulnerabilities.txt"
echo "=================================================="
     remove unnceory  texts and i want clean and for bug bounty i want you to give me and edit and make it for kali linux that in one i can get all and do action above for recon and remove the coments stuff clean
