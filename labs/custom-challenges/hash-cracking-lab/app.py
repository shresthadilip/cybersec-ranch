from flask import Flask, request, render_template_string, redirect, url_for, jsonify
import hashlib
import os

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "CTF{h4sh_cr4ck1ng_m4st3r_j0hn_h4shc4t_8832}")

# Pre-computed challenge hashes:
# admin: "dragon123" -> MD5: e295de8b20967db5be602b9ee77e6827
# sysop: "shadow99" -> SHA256: 41b12b509ef5471c26b528a30dbfce1f9a8a77d341933c0dc89d5337e7a57a07
# backup: "password2026" -> SHA1: 673663a8904df6bce987e914df1bc870dcf4564c
LEAKED_HASHES = [
    {
        "id": 1,
        "username": "admin",
        "hash_type": "MD5",
        "hash_value": "e295de8b20967db5be602b9ee77e6827",
        "plaintext": "dragon123",
        "role": "Super Administrator"
    },
    {
        "id": 2,
        "username": "sysop_internal",
        "hash_type": "SHA-256",
        "hash_value": "41b12b509ef5471c26b528a30dbfce1f9a8a77d341933c0dc89d5337e7a57a07",
        "plaintext": "shadow99",
        "role": "System Operator"
    },
    {
        "id": 3,
        "username": "backup_agent",
        "hash_type": "SHA-1",
        "hash_value": "673663a8904df6bce987e914df1bc870dcf4564c",
        "plaintext": "password2026",
        "role": "Automated Backup Daemon"
    }
]

HTML_LAYOUT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>HashVault - Cryptographic Hash Cracking Arena</title>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;800&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-dark: #090e1a;
            --card-bg: #111a2f;
            --border: #1e2c4a;
            --accent: #06b6d4;
            --accent-glow: rgba(6, 182, 212, 0.25);
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
            background: rgba(17, 26, 47, 0.9);
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
            max-width: 1050px;
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
            margin-bottom: 2rem;
            box-shadow: 0 15px 35px -10px rgba(0,0,0,0.6);
        }
        .banner-challenge {
            background: linear-gradient(135deg, rgba(6, 182, 212, 0.1), rgba(168, 85, 247, 0.05));
            border: 1px solid var(--accent);
            padding: 1rem 1.5rem;
            border-radius: 8px;
            margin-bottom: 1.5rem;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            background: #060914;
            border-radius: 8px;
            overflow: hidden;
            margin: 1.25rem 0;
        }
        th, td {
            padding: 1rem;
            text-align: left;
            border-bottom: 1px solid var(--border);
        }
        th { background: #0c1424; color: var(--text-dim); font-size: 0.85rem; }
        .hash-code { font-family: 'JetBrains Mono', monospace; color: #38bdf8; font-size: 0.85rem; word-break: break-all; }
        input, button {
            padding: 0.75rem 1rem;
            border-radius: 8px;
            border: 1px solid var(--border);
            background: #080d1a;
            color: #fff;
            font-family: inherit;
            font-size: 0.95rem;
        }
        input:focus { outline: none; border-color: var(--accent); box-shadow: 0 0 12px var(--accent-glow); }
        button {
            background: var(--accent);
            color: #041217;
            font-weight: 700;
            cursor: pointer;
            border: none;
            transition: all 0.2s;
        }
        button:hover { transform: translateY(-2px); box-shadow: 0 5px 18px var(--accent-glow); }
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
            <span>🔓</span> HASHVAULT // CREDENTIAL CRACKING ARENA
        </div>
        <div style="font-size: 0.85rem; color: var(--text-dim); font-family: 'JetBrains Mono', monospace;">
            OWASP Top 10: A02 Cryptographic Failures
        </div>
    </header>
    <div class="container">
        <div class="banner-challenge">
            <span>🎯 OBJECTIVE:</span> Crack the leaked password hashes for the <strong>admin</strong> user using John the Ripper, Hashcat, or online lookup tools to unlock the system flag!
        </div>

        <div class="card">
            <h2 style="color: #fff; margin-bottom: 0.5rem;">📜 Leaked Corporate Database Shadow Dump</h2>
            <p style="color: var(--text-dim); margin-bottom: 1rem;">The following cryptographic password hashes were extracted from an unencrypted database dump:</p>

            <table>
                <thead>
                    <tr>
                        <th>Username</th>
                        <th>Hash Algorithm</th>
                        <th>Cryptographic Hash</th>
                        <th>Account Role</th>
                    </tr>
                </thead>
                <tbody>
                    {% for h in hashes %}
                    <tr>
                        <td style="font-weight: bold; color: #fff;">{{ h.username }}</td>
                        <td><span style="background: rgba(6,182,212,0.15); border: 1px solid var(--accent); color: var(--accent); padding: 0.2rem 0.5rem; border-radius: 4px; font-size: 0.75rem; font-family: 'JetBrains Mono', monospace;">{{ h.hash_type }}</span></td>
                        <td class="hash-code">{{ h.hash_value }}</td>
                        <td style="color: var(--text-dim); font-size: 0.85rem;">{{ h.role }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>

            <h3 style="color: #fff; margin-top: 2rem; margin-bottom: 0.75rem;">🔑 Submit Cracked Admin Password:</h3>
            <form method="POST" action="/verify" style="display: flex; gap: 1rem; flex-wrap: wrap;">
                <input type="text" name="cracked_password" placeholder="Enter plaintext password for 'admin'..." style="flex: 1; min-width: 300px;" required>
                <button type="submit">Verify Plaintext</button>
            </form>

            {% if feedback %}
            <div style="margin-top: 1.5rem; padding: 1rem; border-radius: 8px; background: {{ '#062817' if success else '#2d0f15' }}; border: 1px solid {{ '#10b981' if success else '#ef4444' }}; color: {{ '#6ee7b7' if success else '#fca5a5' }}; font-weight: 600;">
                {{ feedback | safe }}
            </div>
            {% endif %}

            <div class="hints-box">
                <strong>💡 Hash Cracking Quick Reference:</strong>
                <ul style="margin-left: 1.5rem; margin-top: 0.5rem; line-height: 1.6;">
                    <li>Identify hash type: 32 hex chars = MD5, 40 hex chars = SHA-1, 64 hex chars = SHA-256</li>
                    <li>John the Ripper: <code>john --format=raw-md5 --wordlist=rockyou.txt hashes.txt</code></li>
                    <li>Hashcat: <code>hashcat -m 0 hashes.txt rockyou.txt</code> (MD5)</li>
                    <li>Online lookup: CrackStation, CyberChef, or Hashes.com</li>
                </ul>
            </div>
        </div>
    </div>
    <footer>
        Cybersecurity Training Lab Environment • CTF Challenge: Hash & Password Cracking
    </footer>
</body>
</html>
"""

@app.route('/', methods=['GET'])
def index():
    return render_template_string(HTML_LAYOUT, hashes=LEAKED_HASHES, feedback=None, success=False)

@app.route('/verify', methods=['POST'])
def verify():
    cracked = request.form.get('cracked_password', '').strip()
    admin_pw = "dragon123"
    
    if cracked.lower() == admin_pw:
        feedback = f"🎉 Password Correct! Admin Hash Cracked. Flag: <code style='color:#fff; background:#02140a; padding:0.2rem 0.5rem; border-radius:4px;'>{FLAG}</code>"
        success = True
    else:
        feedback = "❌ Incorrect password. Try checking standard wordlists or online hash lookup databases!"
        success = False
        
    return render_template_string(HTML_LAYOUT, hashes=LEAKED_HASHES, feedback=feedback, success=success)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
