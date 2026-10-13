# 🤠 CyberSec Ranch — Cybersecurity Training & CTF Lab Suite

> *Where vulnerabilities roam free and flags get wrangled.*

A unified, modular, and containerized cybersecurity training ranch featuring 19+ custom targeted CTF challenges alongside standard industry-grade vulnerable web applications (DVWA, OWASP Juice Shop, WebGoat, bWAPP, Mutillidae II, XVWA, DVGA, vAPI) orchestrated with Docker Compose.

---

## 🎯 Included Labs & Applications

### 📦 Implemented Labs & Challenges (Categorized by Difficulty)

#### 🟢 Beginner — Easy
- [x] **CyberSec Ranch Dashboard** (`http://localhost:8000`) — Core management portal, port health monitor, and CTF scoreboard.
- [x] **SQLi Vault** (`http://localhost:9001`) — SQL Injection (UNION extraction, Auth Bypass).
- [x] **NetProbe** (`http://localhost:9005`) — OS Command Injection & Linux system reconnaissance.
- [x] **MediaVault** (`http://localhost:9006`) — Local File Inclusion (LFI), path traversal, and unrestricted upload.
- [x] **Apex Global Bank** (`http://localhost:9007`) — Insecure Direct Object Reference (IDOR/BOLA) and horizontal privilege escalation.
- [x] **HashVault Arena** (`http://localhost:9008`) — MD5, SHA-1, SHA-256 password hash cracking (John / Hashcat).
- [x] **Port Scanning & Recon** (`http://localhost:8088`, SSH `:2222`, FTP `:2121`, SMTP `:2525`, DNS `:5353`) — Nmap port reconnaissance and service enumeration.
- [x] **Anonymous Services** (SMB `:445`, Redis `:6379`, Anon FTP `:2122`) — Unauthenticated Redis dump and public Samba share enumeration.

#### 🟡 Intermediate — Medium
- [x] **XXE Invoicer** (`http://localhost:9009`) — XML External Entity (XXE) injection via invoice parsing, local file reading, and Blind OOB exfiltration.
- [x] **NoSQLi Gateway** (`http://localhost:9010`) — MongoDB operator injection (`$ne`, `$gt`, `$regex`) for authentication bypass and blind data exfiltration.
- [x] **Cloud SSRF Simulator** (`http://localhost:9002`) — Server-Side Request Forgery & AWS IMDSv1/v2 cloud metadata theft.
- [x] **TokenVault (JWT)** (`http://localhost:9003`) — JWT `none` algorithm confusion & weak HMAC secret brute-force.
- [x] **PickleVault Deserialization** (`http://localhost:9011`) — Python Pickle `__reduce__` exploit and unsigned session state tampering for RCE.
- [x] **Race Condition Bank** (`http://localhost:9012`) — Concurrency gap / Limit Overrun (TOCTOU) multi-threaded race exploitation.
- [x] **CORS & CSRF Portal** (`http://localhost:9014`) — Permissive CORS origin reflection, credential theft, and Cross-Site Request Forgery exploitation sandbox.
- [x] **Linux Privilege Escalation Arena** (SSH `:2223`) — SUID abuse, Sudoers NOPASSWD Python3, and world-writable cron jobs.
- [x] **DVWA (Damn Vulnerable Web App)** (`http://localhost:8081`) — Classic PHP/MySQL OWASP Top 10 with 4 difficulty levels.
- [x] **bWAPP** (`http://localhost:8082`) — Over 100+ classic web vulnerabilities.
- [x] **OWASP Mutillidae II** (`http://localhost:8083`) — In-depth web pen-testing target with inline hints.
- [x] **XVWA** (`http://localhost:8084`) — PHP Object Injection, Session Fixation, XSS, SQLi.
- [x] **vAPI (Vulnerable REST API)** (`http://localhost:8085`) — OWASP API Top 10 (BOLA, Mass Assignment, Auth).

#### 🔴 Advanced — Hard / PWN
- [x] **SSTI Templater** (`http://localhost:9004`) — Jinja2 Server-Side Template Injection & Python sandbox escape.
- [x] **GraphQL API Vault** (`http://localhost:9013`) — GraphQL introspection, hidden `vaultInspection` schemas, and private mutations.
- [x] **Buffer Overflow Arena (PWN)** (TCP `:9015`) — Classic 64-bit stack smashing, `gets()` buffer overflow, and `ret2win` binary exploitation.
- [x] **WebSocket Chat Hijack** (`http://localhost:9016`) — Cross-Site WebSocket Hijacking (CSWSH) and unauthenticated origin sniff attack.
- [x] **DVGA (Damn Vulnerable GraphQL App)** (`http://localhost:5013`) — GraphQL Introspection, Query Batching, DoS, IDOR.
- [x] **OWASP Juice Shop** (`http://localhost:3001`) — Modern Angular/Node.js app with 100+ challenge scoreboard.
- [x] **OWASP WebGoat & WebWolf** (`http://localhost:8080/WebGoat`, `http://localhost:9090/WebWolf`) — Guided interactive lessons and attacker mail receiver.

---

## 🎯 Docker Profiles & Service Overview

The environment is segmented into **Docker Compose Profiles** to prevent resource contention:

| Profile | Application / Lab | Default Port | Status | Vulnerabilities & Focus Areas |
| :--- | :--- | :--- | :---: | :--- |
| **`core`** | **CyberSec Ranch Dashboard** | `http://localhost:8000` | ✅ Active | Management portal, live port checks, OWASP matrix, flag verifier |
| **`custom-ctf`** | **SQLi Vault** | `http://localhost:9001` | ✅ Active | SQL Injection (UNION extraction, Auth Bypass) |
| **`custom-ctf`** | **Cloud SSRF Simulator** | `http://localhost:9002` | ✅ Active | Server-Side Request Forgery & AWS IMDSv1/v2 credentials |
| **`custom-ctf`** | **TokenVault (JWT)** | `http://localhost:9003` | ✅ Active | JWT Algorithm `none` confusion & weak secret brute-force |
| **`custom-ctf`** | **SSTI Templater** | `http://localhost:9004` | ✅ Active | Jinja2 Server-Side Template Injection & Python sandbox escape |
| **`custom-ctf`** | **NetProbe (Cmd Injection)** | `http://localhost:9005` | ✅ Active | OS Command Injection & Linux system reconnaissance |
| **`custom-ctf`** | **MediaVault (File Upload & LFI)**| `http://localhost:9006` | ✅ Active | Local File Inclusion (LFI), path traversal, unrestricted upload |
| **`custom-ctf`** | **Apex Global Bank (IDOR/BOLA)**| `http://localhost:9007` | ✅ Active | Insecure Direct Object Reference, object tampering, financial APIs |
| **`custom-ctf`** | **HashVault Cracking Arena**| `http://localhost:9008` | ✅ Active | MD5, SHA-256, SHA-1 password hash cracking (John / Hashcat) |
| **`custom-ctf`** | **XXE Invoicer** | `http://localhost:9009` | ✅ Active | XML External Entity, file exfiltration, blind DTD injection |
| **`custom-ctf`** | **NoSQLi Gateway** | `http://localhost:9010` | ✅ Active | MongoDB JSON operator injection (`$ne`, `$regex` blind extraction) |
| **`custom-ctf`** | **Insecure Deserialization** | `http://localhost:9011` | ✅ Active | Python Pickle `__reduce__` cookie tampering & Remote Code Execution |
| **`custom-ctf`** | **Race Condition Bank** | `http://localhost:9012` | ✅ Active | Concurrency limit overrun, double spending coupon abuse |
| **`custom-ctf`** | **GraphQL API Vault** | `http://localhost:9013` | ✅ Active | Introspection schema dumping, query batching, private mutations |
| **`custom-ctf`** | **CORS & CSRF Portal** | `http://localhost:9014` | ✅ Active | Permissive origin reflection, credential theft, CSRF exploit |
| **`custom-ctf`** | **Buffer Overflow Arena** | `TCP :9015` | ✅ Active | 64-bit stack smashing, `gets()` buffer overflow, Ret2Win PWN |
| **`custom-ctf`** | **WebSocket Chat Hijack** | `http://localhost:9016` | ✅ Active | Cross-Site WebSocket Hijacking (CSWSH) without origin check |
| **`custom-ctf`** | **Port Scanning & Service Recon** | `http://localhost:8088`<br>*(SSH :2222, FTP :2121, SMTP :2525, DNS :5353)* | ✅ Active | Nmap port scanning, service banner grabbing, protocol enumeration |
| **`custom-ctf`** | **Anonymous & Misconfigured Services**| *(SMB :445, Redis :6379, Anon FTP :2122)* | ✅ Active | Unauthenticated Redis key dumping, anonymous Samba shares |
| **`custom-ctf`** | **Linux Privilege Escalation Arena** | *(SSH :2223 — student:student123)* | ✅ Active | SUID abuse, Sudoers NOPASSWD python3, world-writable root cron |
| **`web-classic`** | **DVWA** | `http://localhost:8081` | ✅ Active | Classic PHP/MySQL OWASP Top 10 with 4 difficulty levels |
| **`web-classic`** | **bWAPP** | `http://localhost:8082` | ✅ Active | Over 100+ web bugs & vulnerabilities |
| **`web-classic`** | **OWASP Mutillidae II** | `http://localhost:8083` | ✅ Active | In-depth web pen-testing target with inline hints |
| **`web-classic`** | **XVWA** | `http://localhost:8084` | ✅ Active | PHP Object Injection, Session Fixation, XSS, SQLi |
| **`web-modern`** | **OWASP Juice Shop** | `http://localhost:3001` | ✅ Active | Modern Angular/Node.js app with 100+ challenge scoreboard |
| **`web-modern`** | **OWASP WebGoat & WebWolf**| `http://localhost:8080/WebGoat`<br>`http://localhost:9090/WebWolf` | ✅ Active | Guided interactive security lessons & mail receiver |
| **`api-graphql`** | **DVGA (GraphQL)** | `http://localhost:5013` | ✅ Active | GraphQL Introspection, Query Batching, DoS, IDOR |
| **`api-graphql`** | **vAPI (REST API)** | `http://localhost:8085` | ✅ Active | OWASP API Top 10 (BOLA, Mass Assignment, Auth) |

---

## 🚀 Quick Start

### 1. Prerequisites
- [Docker](https://docs.docker.com/get-docker/) (Docker Engine or Docker Desktop)
- Docker Compose v2 (`docker compose`)

### 2. Launch Specific Profiles
Run the launcher script or standard `docker compose` commands:

#### On Windows (PowerShell):
```powershell
# Launch the Custom CTF Challenges + Dashboard (Lightweight & Fast)
.\launch.ps1 -Profile custom-ctf

# Launch Classic Labs (DVWA, bWAPP, Mutillidae, XVWA)
.\launch.ps1 -Profile web-classic

# Launch Modern Labs (Juice Shop, WebGoat)
.\launch.ps1 -Profile web-modern

# Launch API & GraphQL Labs
.\launch.ps1 -Profile api-graphql

# Stop and clean up all labs
.\launch.ps1 -Action down
```

#### On Linux / macOS / WSL:
```bash
chmod +x launch.sh

# Start Custom CTF Labs
./launch.sh custom-ctf

# Start Classic Web Labs
./launch.sh web-classic

# Stop everything
./launch.sh down
```

#### Using Docker Compose Directly:
```bash
# Start a specific profile
docker compose --profile custom-ctf up -d

# Start everything (Requires ~6-8GB RAM)
docker compose --profile all up -d

# Stop all containers
docker compose --profile all down
```

---

## 🖥️ CyberSec Ranch Portal & Dashboard
Once launched, open **[http://localhost:8000](http://localhost:8000)** in your browser to access:
- Dynamic port connectivity tester
- Default credentials and setup guides
- Interactive hints and vulnerability breakdowns
- CTF Flag submission & score tracker

---

## 📚 Documentation
- 📖 [Getting Started & Setup Guide](file:///d:/Projects/neuron/personal/CTF/docs/GETTING_STARTED.md)
- 🛡️ [OWASP Top 10 Mapping Matrix](file:///d:/Projects/neuron/personal/CTF/docs/OWASP_TOP10_MAPPING.md)
- 🎯 [Lab Solutions & Exploitation Guide](file:///d:/Projects/neuron/personal/CTF/docs/LAB_SOLUTIONS_GUIDE.md)

---

> [!CAUTION]
> These applications contain intentional security vulnerabilities. Do NOT deploy these containers to public cloud environments or accessible networks without proper network firewalls and isolation.
