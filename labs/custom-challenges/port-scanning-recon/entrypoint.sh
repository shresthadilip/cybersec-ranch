#!/usr/bin/env bash
set -e

echo "[+] Starting Multi-Service Reconnaissance Lab Daemons..."

# Initialize SSH host keys if not generated
ssh-keygen -A 2>/dev/null || true

# Start Services
service ssh start
service nginx start
service vsftpd start
service postfix start
service named start

echo "[✓] All 5 services (SSH, HTTP, FTP, SMTP, DNS) are active and listening!"

# Keep container running and stream syslog if available or idle wait
exec tail -f /dev/null
