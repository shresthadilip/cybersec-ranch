from flask import Flask, request, render_template_string, jsonify
import urllib.request
import urllib.parse
import os
import threading

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "CTF{55rf_cl0ud_m3t4d4t4_3xf1ltr4t10n_9921}")

# Internal Mock Metadata App running locally on loopback 127.0.0.1:8089
internal_app = Flask("internal_service")

@internal_app.route('/latest/meta-data/')
def metadata_root():
    return "iam/\nhostname\ninstance-id\nlocal-ipv4\npublic-keys/\nsecurity-groups"

@internal_app.route('/latest/meta-data/iam/security-credentials/')
def metadata_iam():
    return "s3-backup-admin-role"

@internal_app.route('/latest/meta-data/iam/security-credentials/s3-backup-admin-role')
def metadata_creds():
    return jsonify({
        "Code": "Success",
        "LastUpdated": "2026-09-23T23:50:00Z",
        "Type": "AWS-HMAC",
        "AccessKeyId": "ASIAVULNERABLEKEY9921",
        "SecretAccessKey": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
        "Token": "AQoDYXdzEJr1...",
        "Flag": FLAG,
        "Message": "CRITICAL: Cloud IAM role exfiltrated via SSRF!"
    })

@internal_app.route('/internal-admin')
def internal_admin():
    return jsonify({
        "status": "authorized",
        "internal_note": "Confidential Internal Cluster Admin Panel",
        "flag": FLAG
    })

def start_internal_server():
    internal_app.run(host='127.0.0.1', port=8089, debug=False)

HTML_LAYOUT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CloudSync - Enterprise Webhook & URL Previewer</title>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;800&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-dark: #0a0f1d;
            --card-bg: #111a2e;
            --border: #1e2d4a;
            --accent: #38bdf8;
            --accent-glow: rgba(56, 189, 248, 0.25);
            --text-main: #f1f5f9;
            --text-dim: #94a3b8;
            --success: #10b981;
            --danger: #f43f5e;
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
            background: rgba(17, 26, 46, 0.9);
            backdrop-filter: blur(12px);
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
            margin: 2.5rem auto;
            padding: 0 1rem;
            flex: 1;
            width: 100%;
        }
        .card {
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 2rem;
            box-shadow: 0 15px 35px -10px rgba(0,0,0,0.6);
            margin-bottom: 2rem;
        }
        .banner-challenge {
            background: linear-gradient(135deg, rgba(56, 189, 248, 0.08), rgba(16, 185, 129, 0.05));
            border: 1px solid var(--accent);
            padding: 1rem 1.5rem;
            border-radius: 8px;
            margin-bottom: 1.5rem;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
        }
        input, button {
            padding: 0.85rem 1.25rem;
            border-radius: 8px;
            border: 1px solid var(--border);
            background: #070c18;
            color: #fff;
            font-family: inherit;
            font-size: 0.95rem;
        }
        input:focus { outline: none; border-color: var(--accent); box-shadow: 0 0 12px var(--accent-glow); }
        button {
            background: var(--accent);
            color: #040814;
            font-weight: 700;
            cursor: pointer;
            border: none;
            transition: all 0.2s;
        }
        button:hover { transform: translateY(-2px); box-shadow: 0 5px 18px var(--accent-glow); }
        .response-box {
            background: #050811;
            padding: 1.25rem;
            border-radius: 8px;
            border: 1px solid #1e293b;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
            color: #a5f3fc;
            white-space: pre-wrap;
            word-break: break-all;
            max-height: 400px;
            overflow-y: auto;
            margin-top: 1rem;
        }
        .hints-box {
            background: #090e1a;
            border-left: 4px solid var(--accent);
            padding: 1rem 1.25rem;
            border-radius: 0 8px 8px 0;
            font-size: 0.85rem;
            color: var(--text-dim);
            margin-top: 1.5rem;
        }
        .hints-box code { color: #facc15; font-family: 'JetBrains Mono', monospace; }
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
            <span>🌐</span> SSRF CLOUD LAB // METADATA EXPLOITATION
        </div>
        <div style="font-size: 0.85rem; color: var(--text-dim); font-family: 'JetBrains Mono', monospace;">
            OWASP Top 10: A10 Server-Side Request Forgery
        </div>
    </header>
    <div class="container">
        <div class="banner-challenge">
            <span>🎯 OBJECTIVE:</span> Leverage the URL fetcher to pivot into the server's internal localhost services (port <code>8089</code>) or simulated cloud metadata endpoint to dump AWS IAM credentials containing the flag!
        </div>

        <div class="card">
            <h2 style="color: #fff; margin-bottom: 0.5rem;">Webhook & HTTP Resource Fetcher</h2>
            <p style="color: var(--text-dim); margin-bottom: 1.5rem;">Enter a public or internal URL for the server worker to fetch and inspect.</p>
            
            <form method="POST" action="/" style="display: flex; gap: 1rem; flex-wrap: wrap;">
                <input type="text" name="target_url" placeholder="http://example.com or http://127.0.0.1:8089/latest/meta-data/" value="{{ target_url }}" style="flex: 1; min-width: 300px;" required>
                <button type="submit">Fetch Resource</button>
            </form>

            {% if fetched_content is not none %}
            <div style="margin-top: 2rem;">
                <h4 style="color: #fff; margin-bottom: 0.5rem;">Server Response:</h4>
                <div class="response-box">{{ fetched_content }}</div>
            </div>
            {% endif %}

            <div class="hints-box">
                <strong>💡 Target Endpoints & Hints:</strong>
                <ul style="margin-left: 1.5rem; margin-top: 0.5rem; line-height: 1.6;">
                    <li>Internal Admin: <code>http://127.0.0.1:8089/internal-admin</code></li>
                    <li>AWS IMDSv1 Emulation: <code>http://127.0.0.1:8089/latest/meta-data/iam/security-credentials/s3-backup-admin-role</code></li>
                    <li>Try URL schemes or local aliases (e.g. <code>localhost</code>, <code>127.0.0.1</code>, <code>0.0.0.0</code>)</li>
                </ul>
            </div>
        </div>
    </div>
    <footer>
        Cybersecurity Training Lab Environment • CTF Challenge: SSRF & Cloud Pivoting
    </footer>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    fetched_content = None
    target_url = ""
    if request.method == 'POST':
        target_url = request.form.get('target_url', '')
        try:
            req = urllib.request.Request(
                target_url,
                headers={'User-Agent': 'CloudSync-Bot/2.0 (+http://cloudsync.corp/bot)'}
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                raw_data = response.read()
                try:
                    fetched_content = raw_data.decode('utf-8')
                except UnicodeDecodeError:
                    fetched_content = f"<Binary Data: {len(raw_data)} bytes>"
        except Exception as e:
            fetched_content = f"Error fetching URL '{target_url}': {str(e)}"
            
    return render_template_string(HTML_LAYOUT, fetched_content=fetched_content, target_url=target_url)

if __name__ == '__main__':
    t = threading.Thread(target=start_internal_server, daemon=True)
    t.start()
    app.run(host='0.0.0.0', port=5000, debug=False)
