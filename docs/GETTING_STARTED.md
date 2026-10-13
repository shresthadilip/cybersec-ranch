# Getting Started with CyberSec Ranch

This guide will help you install, configure, and operate the Docker cybersecurity training lab environment.

## 1. System Requirements

- **Operating System**: Windows 10/11 (with WSL2), macOS, or Linux (Ubuntu, Debian, Fedora, Arch)
- **Docker**: Docker Desktop (Windows/macOS) or Docker Engine + Docker Compose v2 (Linux)
- **RAM Recommendations**:
  - Minimum 4 GB RAM for running single profiles (`custom-ctf` or `web-classic`)
  - 8 GB+ RAM for running multiple profiles simultaneously
  - 16 GB RAM for running `all` profiles concurrently

---

## 2. Environment Configuration

All exposed ports and secret CTF flags can be customized in `.env`:

```env
# Change dashboard port if 8000 is occupied
PORT_DASHBOARD=8000

# Classic Web Applications
PORT_DVWA=8081
PORT_BWAPP=8082
PORT_MUTILLIDAE=8083
PORT_XVWA=8084

# Modern Web Applications
PORT_JUICESHOP=3001
PORT_WEBGOAT=8080
PORT_WEBWOLF=9090

# Custom CTF Challenges
PORT_CTF_SQLI=9001
PORT_CTF_SSRF=9002
PORT_CTF_JWT=9003
PORT_CTF_SSTI=9004
PORT_CTF_CMD=9005
PORT_CTF_UPLOAD=9006
PORT_CTF_IDOR=9007
PORT_CTF_HASH=9008

# Network Reconnaissance & Anonymous Services
PORT_RECON_SSH=2222
PORT_RECON_HTTP=8088
PORT_RECON_FTP=2121
PORT_RECON_SMTP=2525
PORT_RECON_DNS=5353
PORT_SMB=445
PORT_REDIS=6379
PORT_ANON_FTP=2122

# Linux Privilege Escalation Lab
PORT_PRIVESC_SSH=2223
```

---

## 3. Initializing Classic Labs (First Launch Database Setup)

Some classic PHP/MySQL applications require a one-click database initialization on their first launch:

### 1. DVWA (`http://localhost:8081`)
- When the page opens, scroll down to the bottom and click **"Create / Reset Database"**.
- Default login:
  - **Username**: `admin`
  - **Password**: `password`
- Change vulnerability difficulty level under **DVWA Security** in the sidebar.

### 2. bWAPP (`http://localhost:8082/install.php`)
- Visit `http://localhost:8082/install.php` and click the **"here"** link to create the tables.
- Default login:
  - **Username**: `bee`
  - **Password**: `bug`

### 3. Mutillidae II (`http://localhost:8083`)
- If a database connection error appears, click **"Setup / reset the DB"** in the top navigation bar.
- Default login:
  - **Username**: `admin`
  - **Password**: `adminpass`

### 4. XVWA (`http://localhost:8084/xvwa/setup/`)
- Visit `http://localhost:8084/xvwa/setup/` and click **"Setup / Reset Database"**.
- Default login:
  - **Username**: `admin`
  - **Password**: `admin`

---

## 4. Running the Dashboard Standalone (No Docker Required)

If you just want to preview or run the dashboard UI locally without Docker:
```bash
python dashboard/server.py
```
Open [http://localhost:8000](http://localhost:8000).
