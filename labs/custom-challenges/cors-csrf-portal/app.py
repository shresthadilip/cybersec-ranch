from flask import Flask, request, jsonify, render_template_string, make_response, redirect
import os

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "CTF{c0rs_m1sc0nf1g_cr3d3nt14l_th3ft_4419}")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Aura Security // CORS & CSRF Lab</title>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;800&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg: #090e17;
            --card: #121927;
            --border: #1e2a3f;
            --accent: #8b5cf6;
            --accent-glow: rgba(139, 92, 246, 0.25);
            --text: #f8fafc;
            --text-dim: #94a3b8;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            background-color: var(--bg);
            color: var(--text);
            font-family: 'Inter', sans-serif;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }
        header {
            background: rgba(18, 25, 39, 0.95);
            border-bottom: 1px solid var(--border);
            padding: 1.25rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .brand {
            font-family: 'JetBrains Mono', monospace;
            font-size: 1.2rem;
            font-weight: 800;
            color: var(--accent);
        }
        .container {
            max-width: 1050px;
            margin: 2rem auto;
            padding: 0 1rem;
            flex: 1;
            width: 100%;
        }
        .banner {
            background: linear-gradient(135deg, rgba(139, 92, 246, 0.1), rgba(109, 40, 217, 0.05));
            border: 1px solid var(--accent);
            padding: 1rem 1.5rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
            line-height: 1.5;
        }
        .grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1.5rem;
        }
        .card {
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
        }
        h2 { font-size: 1.15rem; margin-bottom: 0.75rem; color: #fff; }
        p { color: var(--text-dim); font-size: 0.85rem; margin-bottom: 1rem; }
        .data-row {
            display: flex;
            justify-content: space-between;
            padding: 0.6rem 0;
            border-bottom: 1px solid #1e293b;
            font-size: 0.85rem;
        }
        .data-label { color: var(--text-dim); }
        .data-val { font-family: 'JetBrains Mono', monospace; color: #a78bfa; font-weight: 600; }
        button, .link-btn {
            background: var(--accent);
            color: #fff;
            font-weight: 700;
            padding: 0.75rem 1.25rem;
            border-radius: 8px;
            border: none;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            transition: all 0.2s;
            text-align: center;
        }
        button:hover, .link-btn:hover { transform: translateY(-2px); box-shadow: 0 5px 15px var(--accent-glow); }
        footer {
            text-align: center;
            padding: 1.5rem;
            color: var(--text-dim);
            font-size: 0.8rem;
            border-top: 1px solid var(--border);
        }
    </style>
</head>
<body>
    <header>
        <div class="brand">🌐 AURA IDENTITY // CORS & CSRF LAB</div>
        <div style="font-size: 0.85rem; color: var(--text-dim); font-family: 'JetBrains Mono', monospace;">OWASP A01: Broken Access Control (CORS Misconfiguration)</div>
    </header>

    <div class="container">
        <div class="banner">
            🎯 <strong>MISSION:</strong> The backend profile API reflects any supplied <code>Origin</code> header with <code>Access-Control-Allow-Credentials: true</code>.<br>
            • Switch to the simulated <strong>Attacker Exploit Sandbox</strong>.<br>
            • Craft a cross-origin JavaScript payload that sends a credentialed request to <code>/api/profile</code> and exfiltrates the victim's private flag!
        </div>

        <div class="grid">
            <!-- Authenticated Profile Card -->
            <div class="card">
                <h2>👤 Authenticated User Profile (Victim)</h2>
                <p>Simulating a logged-in user with an active HTTP session cookie.</p>
                <div class="data-row">
                    <span class="data-label">Account Holder:</span>
                    <span class="data-val">Chief Executive Admin</span>
                </div>
                <div class="data-row">
                    <span class="data-label">Email:</span>
                    <span class="data-val">ceo@aurasecurity.internal</span>
                </div>
                <div class="data-row">
                    <span class="data-label">Account Balance:</span>
                    <span class="data-val">$2,450,000.00 USD</span>
                </div>
                <div class="data-row">
                    <span class="data-label">Vault Flag:</span>
                    <span class="data-val">{{ flag }}</span>
                </div>
                <div class="data-row">
                    <span class="data-label">Session Cookie:</span>
                    <span class="data-val">aura_auth_session=admin_secure_cookie_9981</span>
                </div>
            </div>

            <!-- Exploit Sandbox Navigation -->
            <div class="card" style="display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <h2>🏴‍☠️ Attacker Exploit Sandbox</h2>
                    <p>Open the external simulated attacker web application. This domain simulates <code>http://attacker-controlled-site.com</code> to launch cross-origin exploits.</p>
                </div>
                <div>
                    <a href="/attacker-sandbox" class="link-btn" style="width: 100%;">Open Attacker Sandbox 🚀</a>
                </div>
            </div>
        </div>
    </div>

    <footer>
        CyberSec Range • Cross-Origin Resource Sharing (CORS) Misconfiguration Challenge
    </footer>
</body>
</html>
"""

ATTACKER_SANDBOX_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Attacker Exploit Sandbox // Evil Domain</title>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;800&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg: #110c1f;
            --card: #1a122e;
            --border: #2e2050;
            --accent: #ec4899;
            --accent-glow: rgba(236, 72, 153, 0.25);
            --text: #f8fafc;
            --text-dim: #a78bfa;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            background-color: var(--bg);
            color: var(--text);
            font-family: 'Inter', sans-serif;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }
        header {
            background: rgba(26, 18, 46, 0.95);
            border-bottom: 1px solid var(--border);
            padding: 1.25rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .brand {
            font-family: 'JetBrains Mono', monospace;
            font-size: 1.2rem;
            font-weight: 800;
            color: var(--accent);
        }
        .container {
            max-width: 1000px;
            margin: 2rem auto;
            padding: 0 1rem;
            flex: 1;
            width: 100%;
        }
        .card {
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
            margin-bottom: 1.5rem;
        }
        textarea {
            width: 100%;
            height: 180px;
            background: #0b0716;
            border: 1px solid var(--border);
            border-radius: 8px;
            color: #f472b6;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
            padding: 1rem;
            resize: vertical;
        }
        textarea:focus { outline: none; border-color: var(--accent); box-shadow: 0 0 10px var(--accent-glow); }
        button {
            background: var(--accent);
            color: #fff;
            font-weight: 700;
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            border: none;
            cursor: pointer;
            margin-top: 1rem;
        }
        .output {
            background: #05030a;
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 1rem;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
            color: #4ade80;
            min-height: 100px;
            white-space: pre-wrap;
            word-break: break-all;
        }
    </style>
</head>
<body>
    <header>
        <div class="brand">🏴‍☠️ SIMULATED ATTACKER SITE // EVIL.COM</div>
        <a href="/" style="color: var(--text-dim); text-decoration: none; font-size: 0.85rem;">← Back to Victim Portal</a>
    </header>

    <div class="container">
        <div class="card">
            <h2 style="margin-bottom: 0.5rem; color: #fff;">Cross-Origin Exploit Generator</h2>
            <p style="color: var(--text-dim); font-size: 0.85rem; margin-bottom: 1rem;">Execute a credentialed <code>fetch()</code> request with <code>credentials: 'include'</code> against the victim's API endpoint.</p>
            
            <textarea id="exploitCode">// Cross-Origin Credentialed Request Payload
fetch('/api/profile', {
    method: 'GET',
    credentials: 'include',
    headers: {
        'Origin': 'https://evil-hacker-domain.com'
    }
})
.then(response => response.json())
.then(data => {
    document.getElementById('stolenOutput').textContent = '✅ EXPLOIT SUCCESSFUL! Stolen Data:\\n' + JSON.stringify(data, null, 2);
})
.catch(err => {
    document.getElementById('stolenOutput').textContent = '❌ Request failed: ' + err;
});</textarea>
            
            <button onclick="runExploit()">Trigger Cross-Origin Exploit 💥</button>
        </div>

        <div class="card">
            <h3 style="margin-bottom: 0.5rem; color: #fff;">📡 Siphoned Data / Exfiltration Log</h3>
            <div class="output" id="stolenOutput">// Stolen victim profile data will be logged here...</div>
        </div>
    </div>

    <script>
        function runExploit() {
            const code = document.getElementById('exploitCode').value;
            try {
                eval(code);
            } catch(e) {
                document.getElementById('stolenOutput').textContent = 'Syntax/Execution Error: ' + e.message;
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    resp = make_response(render_template_string(HTML_TEMPLATE, flag="REDACTED_IN_PUBLIC_DOM (Inspect via API)"))
    resp.set_cookie('aura_auth_session', 'admin_secure_cookie_9981', httponly=False)
    return resp

@app.route('/attacker-sandbox')
def attacker_sandbox():
    return render_template_string(ATTACKER_SANDBOX_TEMPLATE)

@app.route('/api/profile', methods=['GET', 'OPTIONS'])
def api_profile():
    origin = request.headers.get('Origin', '*')
    
    # VULNERABILITY: Overly permissive CORS with credentials
    resp = jsonify({
        "status": "success",
        "user": {
            "account_id": "ACC-99218-VIP",
            "name": "Chief Executive Admin",
            "email": "ceo@aurasecurity.internal",
            "role": "SuperAdministrator",
            "balance": 2450000.00,
            "confidential_flag": FLAG
        }
    })
    
    # Set vulnerable CORS headers
    resp.headers['Access-Control-Allow-Origin'] = origin
    resp.headers['Access-Control-Allow-Credentials'] = 'true'
    resp.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    resp.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
