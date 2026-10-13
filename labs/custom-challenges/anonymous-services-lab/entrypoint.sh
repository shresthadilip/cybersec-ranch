#!/usr/bin/env bash
set -e

echo "[+] Starting Anonymous & Misconfigured Services Daemons..."

# 1. Start Redis in background and populate CTF keys
redis-server --protected-mode no --daemonize yes
sleep 1
redis-cli set "company_motto" "Security by Obscurity is our Promise"
redis-cli set "internal_admin_token" "token_99218_auth_bypass"
redis-cli set "flag" "CTF{r3d15_un4uth_k3y_dumP_3xpl01t_992}"
redis-cli hset "user:1" "username" "admin" "role" "superuser" "api_key" "CTF{r3d15_un4uth_k3y_dumP_3xpl01t_992}"

# 2. Start Samba (SMB)
service smbd start
service nmbd start

# 3. Start vsftpd (Anonymous FTP)
service vsftpd start

echo "[✓] Anonymous services (SMB :445, Redis :6379, FTP :21) are running!"

exec tail -f /dev/null
