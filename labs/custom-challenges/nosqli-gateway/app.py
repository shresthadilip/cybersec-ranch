from flask import Flask, request, jsonify, render_template_string
import os
import re

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "CTF{n05ql_1nj3ct10n_m0ng0_0p3r4t0r_pwnd_8812}")

# Mock MongoDB-like database
USERS_DB = [
    {
        "id": 1,
        "username": "admin",
        "password": "SuperSecretAdminPassword_CannotBeGuessed_9921#",
        "role": "SuperAdministrator",
        "secret_token": FLAG,
        "email": "sec-admin@internal-gateway.corp"
    },
    {
        "id": 2,
        "username": "developer",
        "password": "devpassword123",
        "role": "Developer",
        "secret_token": "DEV_TOKEN_xyz9921_not_flag",
        "email": "dev@internal-gateway.corp"
    },
    {
        "id": 3,
        "username": "guest",
        "password": "guestpassword",
        "role": "Viewer",
        "secret_token": "GUEST_TOKEN_abc123",
        "email": "guest@internal-gateway.corp"
    }
]

def evaluate_nosql_condition(stored_val, query_val):
    """Simulates MongoDB query evaluation on a single field."""
    if isinstance(query_val, dict):
        for op, op_val in query_val.items():
            if op == "$ne":
                if stored_val == op_val:
                    return False
            elif op == "$gt":
                if not (str(stored_val) > str(op_val)):
                    return False
            elif op == "$gte":
                if not (str(stored_val) >= str(op_val)):
                    return False
            elif op == "$lt":
                if not (str(stored_val) < str(op_val)):
                    return False
            elif op == "$lte":
                if not (str(stored_val) <= str(op_val)):
                    return False
            elif op == "$regex":
                try:
                    if not re.search(str(op_val), str(stored_val)):
                        return False
                except Exception:
                    return False
            elif op == "$exists":
                exists = stored_val is not None
                if exists != bool(op_val):
                    return False
        return True
    return stored_val == query_val

def find_user(query):
    """Simulates db.users.find_one(query)"""
    for user in USERS_DB:
        match = True
        for key, val in query.items():
            if key not in user or not evaluate_nosql_condition(user[key], val):
                match = False
                break
        if match:
            return user
    return None

def find_users(query):
    """Simulates db.users.find(query)"""
    results = []
    for user in USERS_DB:
        match = True
        for key, val in query.items():
            if key not in user or not evaluate_nosql_condition(user[key], val):
                match = False
                break
        if match:
            results.append(user)
    return results

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NoSQL Gateway // NoSQL Injection Arena</title>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;800&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg: #090d16;
            --card: #111827;
            --border: #1f293d;
            --accent: #10b981;
            --accent-glow: rgba(16, 185, 129, 0.25);
            --text: #f3f4f6;
            --text-dim: #9ca3af;
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
            background: rgba(17, 24, 39, 0.95);
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
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .container {
            max-width: 1000px;
            margin: 2rem auto;
            padding: 0 1rem;
            flex: 1;
            width: 100%;
        }
        .banner {
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(6, 95, 70, 0.05));
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
        h2 { font-size: 1.15rem; margin-bottom: 0.5rem; color: #fff; }
        p { color: var(--text-dim); font-size: 0.85rem; margin-bottom: 1rem; }
        textarea, input {
            width: 100%;
            background: #060913;
            border: 1px solid var(--border);
            border-radius: 8px;
            color: #38bdf8;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
            padding: 0.75rem;
            margin-bottom: 1rem;
        }
        textarea { height: 120px; resize: vertical; }
        textarea:focus, input:focus { outline: none; border-color: var(--accent); box-shadow: 0 0 10px var(--accent-glow); }
        button {
            width: 100%;
            background: var(--accent);
            color: #000;
            font-weight: 700;
            padding: 0.75rem;
            border-radius: 8px;
            border: none;
            cursor: pointer;
            transition: all 0.2s;
            font-family: 'Inter', sans-serif;
        }
        button:hover { transform: translateY(-2px); box-shadow: 0 5px 15px var(--accent-glow); }
        .output {
            margin-top: 1rem;
            background: #030712;
            border: 1px solid #1f2937;
            border-radius: 8px;
            padding: 1rem;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.8rem;
            color: #a7f3d0;
            white-space: pre-wrap;
            word-break: break-all;
            min-height: 80px;
        }
        .endpoint-tag {
            background: #064e3b;
            color: #34d399;
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.75rem;
            display: inline-block;
            margin-bottom: 0.5rem;
        }
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
        <div class="brand">🍃 NoSQL GATEWAY // INJECTION ARENA</div>
        <div style="font-size: 0.85rem; color: var(--text-dim); font-family: 'JetBrains Mono', monospace;">OWASP A03: Injection (NoSQL)</div>
    </header>
    <div class="container">
        <div class="banner">
            🎯 <strong>MISSION:</strong> The authentication and lookup services accept unvalidated JSON dictionary filters directly into MongoDB query functions.<br>
            • <strong>Phase 1 (Auth Bypass):</strong> Inject MongoDB operators like <code>{"$ne": ""}</code> to authenticate as <code>admin</code> without the password.<br>
            • <strong>Phase 2 (Blind Exfiltration):</strong> Leverage <code>{"$regex": "^CTF{..."}</code> on the user lookup endpoint to extract the admin's secret token!
        </div>

        <div class="grid">
            <!-- Auth Gateway -->
            <div class="card">
                <span class="endpoint-tag">POST /api/login</span>
                <h2>Authentication Service</h2>
                <p>Submit JSON credentials. Insecurely executed as <code>find_one(req.json)</code>.</p>
                <textarea id="authJson">{
  "username": "admin",
  "password": { "$ne": "wrongpassword" }
}</textarea>
                <button onclick="submitAuth()">Authenticate Payload 🔑</button>
                <div class="output" id="authOutput">// Response will appear here...</div>
            </div>

            <!-- User Lookup API -->
            <div class="card">
                <span class="endpoint-tag">POST /api/user/lookup</span>
                <h2>User Lookup & Filter API</h2>
                <p>Search user records by attributes or regex patterns against <code>secret_token</code>.</p>
                <textarea id="lookupJson">{
  "username": "admin",
  "secret_token": { "$regex": "^CTF{.*" }
}</textarea>
                <button onclick="submitLookup()">Query Database 🔍</button>
                <div class="output" id="lookupOutput">// Search results will appear here...</div>
            </div>
        </div>
    </div>

    <footer>
        CyberSec Range • NoSQL Injection & MongoDB Operator Tampering Challenge
    </footer>

    <script>
        async function submitAuth() {
            const out = document.getElementById('authOutput');
            out.textContent = 'Sending payload...';
            try {
                const payload = JSON.parse(document.getElementById('authJson').value);
                const res = await fetch('/api/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const data = await res.json();
                out.textContent = JSON.stringify(data, null, 2);
            } catch (err) {
                out.textContent = 'Error: ' + err.message;
            }
        }

        async function submitLookup() {
            const out = document.getElementById('lookupOutput');
            out.textContent = 'Executing query...';
            try {
                const payload = JSON.parse(document.getElementById('lookupJson').value);
                const res = await fetch('/api/user/lookup', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const data = await res.json();
                out.textContent = JSON.stringify(data, null, 2);
            } catch (err) {
                out.textContent = 'Error: ' + err.message;
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/login', methods=['POST'])
def api_login():
    try:
        query = request.get_json(force=True)
        if not query or not isinstance(query, dict):
            return jsonify({"status": "error", "message": "Invalid JSON body"}), 400
        
        # Vulnerable NoSQL Query
        user = find_user(query)
        if user:
            return jsonify({
                "status": "success",
                "message": f"Welcome back, {user['username']}!",
                "user": {
                    "id": user["id"],
                    "username": user["username"],
                    "role": user["role"],
                    "email": user["email"]
                },
                "hint": "Admin login bypassed successfully! Now extract the secret_token via /api/user/lookup using $regex."
            }), 200
        else:
            return jsonify({"status": "error", "message": "Invalid credentials"}), 401
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/user/lookup', methods=['POST'])
def api_lookup():
    try:
        query = request.get_json(force=True)
        if not query or not isinstance(query, dict):
            return jsonify({"status": "error", "message": "Invalid JSON filter"}), 400
        
        matches = find_users(query)
        # Return sanitized summary
        results = []
        for m in matches:
            results.append({
                "id": m["id"],
                "username": m["username"],
                "role": m["role"],
                "email": m["email"],
                "token_preview": m["secret_token"] if m["username"] != "admin" else "REDACTED [Use regex blind extraction to uncover full string]"
            })
            if m["username"] == "admin" and "secret_token" in query:
                # If exact full match passed or regex matched, provide flag when full string verified
                if query["secret_token"] == FLAG or (isinstance(query["secret_token"], dict) and query["secret_token"].get("$regex") == f"^{FLAG}$"):
                    results[0]["token_revealed"] = FLAG
        
        return jsonify({
            "status": "success",
            "matched_count": len(matches),
            "results": results
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
