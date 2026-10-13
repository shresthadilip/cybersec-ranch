# OWASP Top 10 (2021) & API Security Top 10 Mapping Matrix

This matrix correlates each vulnerability class with the respective labs in the CyberSec Ranch collection.

---

## OWASP Top 10 Web Application Security Risks (2021)

| OWASP ID | Vulnerability Category | Primary Practice Labs | Attack Concepts & Exercises |
| :--- | :--- | :--- | :--- |
| **A01:2021** | **Broken Access Control** | • Juice Shop<br>• Apex Global Bank (IDOR)<br>• MediaVault (LFI)<br>• TokenVault (JWT)<br>• Aura Identity (CORS/CSRF)<br>• Aether Ops (CSWSH)<br>• Linux PrivEsc Arena<br>• Mutillidae II<br>• DVWA | IDOR / BOLA, Permissive CORS Origin Reflection, Cross-Site WebSocket Hijacking, SUID / Sudoers Abuse, Unrestricted LFI |
| **A02:2021** | **Cryptographic Failures** | • TokenVault (JWT)<br>• HashVault Cracking Arena<br>• WebGoat<br>• bWAPP | Weak JWT HMAC secrets, Insecure algorithms (`none`), Missing HTTPS/TLS, MD5/SHA-256 password hash cracking |
| **A03:2021** | **Injection** | • SQLi Vault<br>• NoSQL Gateway<br>• SSTI Templater<br>• NetProbe Cmd<br>• MediaVault (LFI)<br>• DVWA<br>• XVWA | SQL Injection (UNION & Auth Bypass), NoSQL Injection (MongoDB Operators), Server-Side Template Injection (Jinja2), OS Command Injection |
| **A04:2021** | **Insecure Design** | • Race Condition Bank<br>• Juice Shop<br>• WebGoat | TOCTOU concurrency gaps, Multi-threaded race condition double spending, Flawed business logic |
| **A05:2021** | **Security Misconfiguration**| • XXE Invoicer<br>• Anonymous Services Lab<br>• Port Scanning Recon<br>• GraphQL Vault<br>• Linux PrivEsc (Cron / SUID)<br>• DVGA (GraphQL)<br>• Mutillidae II | XML External Entity (XXE) entity resolution, Unauthenticated Redis & Anonymous Samba shares, Enabled GraphQL Introspection |
| **A06:2021** | **Vulnerable & Outdated Components** | • Juice Shop<br>• bWAPP | Known vulnerable npm/pip packages, Log4Shell simulation, CVE exploits |
| **A07:2021** | **Identification & Authentication Failures** | • SQLi Auth Bypass<br>• NoSQL Gateway<br>• TokenVault<br>• DVWA (Brute Force) | Credential stuffing, Weak session tokens, NoSQL `$ne` password bypass, Missing rate limiting |
| **A08:2021** | **Software & Data Integrity Failures** | • PickleVault (Deserialization)<br>• XVWA<br>• Juice Shop | Python Pickle `__reduce__` RCE, PHP Object Deserialization, Unsigned session cookie tampering |
| **A09:2021** | **Security Logging & Monitoring Failures** | • WebGoat<br>• vAPI | Missing audit trails for high-value transactions, Log injection |
| **A10:2021** | **Server-Side Request Forgery (SSRF)** | • Cloud SSRF Sim<br>• Juice Shop<br>• WebGoat | Cloud IMDSv1/v2 metadata dumping, Pivoting to internal ports (`127.0.0.1:8089`), Webhook abuse |

---

## OWASP API Security Top 10 (2023)

| API Category | Description | Primary Lab Target |
| :--- | :--- | :--- |
| **API1:2023** | Broken Object Level Authorization (BOLA) | vAPI (`http://localhost:8085`), Apex Global Bank (`http://localhost:9007`), DVGA |
| **API2:2023** | Broken Authentication | TokenVault (`:9003`), NoSQL Gateway (`:9010`), vAPI |
| **API3:2023** | Broken Object Property Level Authorization (Mass Assignment) | vAPI, Juice Shop |
| **API4:2023** | Unrestricted Resource Consumption (DoS / Rate Limiting) | DVGA (GraphQL Circular Queries), Race Condition Bank (`:9012`) |
| **API5:2023** | Broken Function Level Authorization (BFLA) | GraphQL Vault (`:9013`), vAPI, DVGA |
| **API6:2023** | Unrestricted Access to Sensitive Business Flows | Race Condition Bank (`:9012`), Juice Shop |
| **API7:2023** | Server-Side Request Forgery (SSRF) | Cloud SSRF Simulator (`:9002`) |
| **API8:2023** | Security Misconfiguration (Introspection & CORS) | GraphQL Vault (`:9013`), Aura Identity (`:9014`), DVGA |
| **API9:2023** | Improper Inventory Management | GraphQL Vault (`:9013`), vAPI |
| **API10:2023**| Unsafe Consumption of APIs | Aether Ops WebSocket Hijack (`:9016`) |

---

## Binary Exploitation & Systems Security

| Category | Lab Target | Attack Concepts & Exercises |
| :--- | :--- | :--- |
| **PWN / Memory Corruption** | **Buffer Overflow Arena** (`TCP :9015`) | 64-bit stack smashing, `gets()` unbounded buffer overflow, `ret2win` RIP control flow hijacking |
| **OS & Privilege Escalation** | **Linux PrivEsc Arena** (`SSH :2223`) | SUID `/find` execution, Sudoers NOPASSWD `python3`, World-writable root cron job hijacking |
| **Network Protocol Recon** | **Port Scanning Lab** (`:8088`, `:2222`, `:2121`, `:2525`, `:5353`) | Nmap service enumeration, banner grabbing, raw socket interaction |
| **Misconfigured Daemons** | **Anonymous Services Lab** (`:445`, `:6379`, `:2122`) | Unauthenticated Redis memory key extraction, public Samba share enumeration |
