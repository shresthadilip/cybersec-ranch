from flask import Flask, request, render_template_string, redirect, url_for, make_response
import base64
import json
import hmac
import hashlib
import time
import os

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "CTF{jwt_n0n3_4lg_4nd_w34k_s3cr3t_f0rg3ry}")
SECRET_KEY = "secret123"  # Intentionally weak for dictionary attack / brute force

def b64_url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode('utf-8').replace('=', '')

def b64_url_decode(data: str) -> bytes:
    padding = '=' * (4 - (len(data) % 4)) if len(data) % 4 != 0 else ''
    return base64.urlsafe_b64decode(data + padding)

def create_jwt(payload: dict, secret: str, alg="HS256") -> str:
    header = {"typ": "JWT", "alg": alg}
    header_b64 = b64_url_encode(json.dumps(header).encode('utf-8'))
    payload_b64 = b64_url_encode(json.dumps(payload).encode('utf-8'))
    
    if alg.lower() == "none":
        return f"{header_b64}.{payload_b64}."
    
    signature = hmac.new(secret.encode('utf-8'), f"{header_b64}.{payload_b64}".encode('utf-8'), hashlib.sha256).digest()
    sig_b64 = b64_url_encode(signature)
    return f"{header_b64}.{payload_b64}.{sig_b64}"

def verify_jwt(token: str):
    parts = token.split('.')
    if len(parts) < 2:
        return None, "Invalid JWT format"
    
    try:
        header = json.loads(b64_url_decode(parts[0]))
        payload = json.loads(b64_url_decode(parts[1]))
    except Exception as e:
        return None, f"JSON Decode Error: {str(e)}"
    
    alg = header.get('alg', 'HS256')
    
    # Vulnerability 1: Insecure handling of "none" / "None" / "NONE" algorithm
    if alg.lower() == 'none':
        return payload, None
    
    if alg == 'HS256':
        if len(parts) != 3:
            return None, "Missing signature for HS256"
        expected_sig = b64_url_encode(hmac.new(SECRET_KEY.encode('utf-8'), f"{parts[0]}.{parts[1]}".encode('utf-8'), hashlib.sha256).digest())
        if parts[2] != expected_sig:
            return None, "Signature mismatch"
        return payload, None
    
    return None, f"Unsupported algorithm: {alg}"

HTML_LAYOUT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TokenVault - JWT Authentication Security Lab</title>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;800&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-dark: #090c15;
            --card-bg: #121829;
            --border: #1f2a44;
            --accent: #a855f7;
            --accent-glow: rgba(168, 85, 247, 0.25);
            --text-main: #f8fafc;
            --text-dim: #94a3b8;
            --success: #10b981;
            --danger: #ef4444;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            background-color: var(--bg-dark);
            color: var(--text-main);
            font-family: 'Inter', sans-serif;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }
        header {
            border-bottom: 1px solid var(--border);
            padding: 1.25rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: rgba(18, 24, 41, 0.9);
            backdrop-filter: blur(10px);
        }
        .brand {
            font-family: 'JetBrains Mono', monospace;
            font-size: 1.25rem;
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
        .card {
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 2rem;
            box-shadow: 0 10px 30px -10px rgba(0,0,0,0.5);
            margin-bottom: 2rem;
        }
        .banner-challenge {
            background: linear-gradient(135deg, rgba(168, 85, 247, 0.1), rgba(59, 130, 246, 0.05));
            border: 1px solid var(--accent);
            padding: 1rem 1.5rem;
            border-radius: 8px;
            margin-bottom: 1.5rem;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
        }
        input, textarea, button {
            padding: 0.75rem 1rem;
            border-radius: 8px;
            border: 1px solid var(--border);
            background: #080c18;
            color: #fff;
            font-family: inherit;
            font-size: 0.95rem;
        }
        input:focus, textarea:focus { outline: none; border-color: var(--accent); box-shadow: 0 0 12px var(--accent-glow); }
        button {
            background: var(--accent);
            color: #fff;
            font-weight: 700;
            cursor: pointer;
            border: none;
            transition: all 0.2s;
        }
        button:hover { transform: translateY(-2px); box-shadow: 0 5px 18px var(--accent-glow); }
        .token-breakdown {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 1rem;
            margin-top: 1.5rem;
        }
        .token-part {
            background: #070a14;
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 1rem;
        }
        .token-part h4 { font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; margin-bottom: 0.5rem; }
        .token-part pre {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.8rem;
            color: #c084fc;
            white-space: pre-wrap;
            word-break: break-all;
        }
        .alert {
            padding: 0.85rem 1.25rem;
            border-radius: 8px;
            margin-bottom: 1.25rem;
            font-weight: 500;
        }
        .alert-error { background: rgba(239, 68, 68, 0.15); border: 1px solid var(--danger); color: #fca5a5; }
        .alert-success { background: rgba(16, 185, 129, 0.15); border: 1px solid var(--success); color: #6ee7b7; }
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
        <div class="brand">
            <span>🔑</span> TOKENVAULT // JWT EXPLOITATION LAB
        </div>
        <div style="font-size: 0.85rem; color: var(--text-dim); font-family: 'JetBrains Mono', monospace;">
            OWASP Top 10: A07 Identification & Authentication Failures
        </div>
    </header>
    <div class="container">
        <div class="banner-challenge">
            <span>🎯 OBJECTIVE:</span> Forge an authentication token to gain <code>admin</code> privileges! You can either exploit the <code>alg: "none"</code> vulnerability or crack the weak HMAC secret key with dictionary attacks.
        </div>
        {{ content | safe }}
    </div>
    <footer>
        Cybersecurity Training Lab Environment • CTF Challenge: JWT Tampering & Algorithm Confusion
    </footer>
</body>
</html>
"""

@app.route('/')
def index():
    auth_cookie = request.cookies.get('auth_token')
    if not auth_cookie:
        # Assign guest token
        default_payload = {
            "sub": "guest_user",
            "role": "guest",
            "permissions": ["view_public"],
            "iat": int(time.time()),
            "iss": "tokenvault.local"
        }
        token = create_jwt(default_payload, SECRET_KEY)
        resp = make_response(redirect(url_for('index')))
        resp.set_cookie('auth_token', token)
        return resp
    
    payload, err = verify_jwt(auth_cookie)
    
    parts = auth_cookie.split('.')
    header_raw = ""
    payload_raw = ""
    sig_raw = parts[2] if len(parts) > 2 else ""
    try:
        header_raw = json.dumps(json.loads(b64_url_decode(parts[0])), indent=2)
    except:
        header_raw = parts[0]
        
    try:
        payload_raw = json.dumps(json.loads(b64_url_decode(parts[1])), indent=2)
    except:
        payload_raw = parts[1] if len(parts) > 1 else ""

    is_admin = False
    if payload and payload.get('role') == 'admin':
        is_admin = True

    content = f"""
    <div class="card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; flex-wrap: wrap; gap: 1rem;">
            <div>
                <h2 style="color: #fff;">User Session Status</h2>
                <p style="color: var(--text-dim); font-size: 0.9rem;">Current Role: <strong style="color: {'#10b981' if is_admin else 'var(--accent)'};">{payload.get('role') if payload else 'Unverified'}</strong></p>
            </div>
            <div>
                {f"<span class='alert alert-success' style='display: inline-block; margin: 0;'>🛡️ ADMIN ACCESS UNLOCKED</span>" if is_admin else "<span class='alert alert-error' style='display: inline-block; margin: 0;'>🔒 RESTRICTED GUEST ACCESS</span>"}
            </div>
        </div>

        {"<div class='alert alert-error'><strong>Token Error:</strong> " + err + "</div>" if err else ""}

        {f'''
        <div style="background: rgba(16,185,129,0.1); border: 1px solid var(--success); padding: 1.5rem; border-radius: 8px; margin-bottom: 2rem;">
            <h3 style="color: #6ee7b7; margin-bottom: 0.5rem;">🎉 Congratulations! Flag Captured:</h3>
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 1.2rem; font-weight: bold; color: #fff; background: #03140c; padding: 1rem; border-radius: 6px;">{FLAG}</div>
        </div>
        ''' if is_admin else ''}

        <h3 style="color: #fff; margin-bottom: 0.5rem;">Active JWT Breakdown</h3>
        <p style="color: var(--text-dim); font-size: 0.85rem;">Inspect or edit the cookie in your browser / request headers:</p>
        
        <div class="token-breakdown">
            <div class="token-part">
                <h4 style="color: #f43f5e;">HEADER (Algorithm)</h4>
                <pre>{header_raw}</pre>
            </div>
            <div class="token-part">
                <h4 style="color: #a855f7;">PAYLOAD (Claims & Role)</h4>
                <pre>{payload_raw}</pre>
            </div>
            <div class="token-part">
                <h4 style="color: #06b6d4;">SIGNATURE</h4>
                <pre>{sig_raw or '[NONE / UNSIGNED]'}</pre>
            </div>
        </div>

        <div style="margin-top: 2rem; border-top: 1px solid var(--border); padding-top: 1.5rem;">
            <h3 style="color: #fff; margin-bottom: 0.75rem;">Custom Token Submission</h3>
            <form method="POST" action="/submit-token" style="display: flex; flex-direction: column; gap: 1rem;">
                <textarea name="custom_token" rows="3" placeholder="Paste your forged JWT here (header.payload.signature)..." required>{auth_cookie}</textarea>
                <div style="display: flex; gap: 1rem;">
                    <button type="submit">Update Session Token</button>
                    <a href="/reset" style="padding: 0.75rem 1.25rem; border: 1px solid var(--border); color: var(--text-dim); text-decoration: none; border-radius: 8px; font-weight: 600; display: inline-flex; align-items: center;">Reset to Default Guest</a>
                </div>
            </form>
        </div>
    </div>
    """
    return render_template_string(HTML_LAYOUT, content=content)

@app.route('/submit-token', methods=['POST'])
def submit_token():
    token = request.form.get('custom_token', '').strip()
    resp = make_response(redirect(url_for('index')))
    resp.set_cookie('auth_token', token)
    return resp

@app.route('/reset')
def reset():
    resp = make_response(redirect(url_for('index')))
    resp.delete_cookie('auth_token')
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
