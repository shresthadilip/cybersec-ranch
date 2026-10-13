#!/usr/bin/env bash
set -e

echo "[+] Starting Linux Privilege Escalation Arena Daemons..."

# Generate SSH host keys
ssh-keygen -A 2>/dev/null || true

# Start Cron & SSH services
service cron start
service ssh start

echo "[✓] Linux PrivEsc Arena active! Connect via SSH: ssh -p 2223 student@localhost (Password: student123)"

exec tail -f /dev/null
