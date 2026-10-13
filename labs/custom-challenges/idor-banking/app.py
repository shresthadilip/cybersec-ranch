from flask import Flask, request, render_template_string, redirect, url_for, session, jsonify
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

FLAG = os.environ.get("FLAG", "CTF{1d0r_b0l4_pr1v1l3g3_3sc4l4t10n_8821}")

ACCOUNTS = {
    1: {
        "id": 1,
        "owner": "Mr. Sterling (VIP Chairman)",
        "account_type": "Executive Vault & Offshore Reserves",
        "balance": 15450000.00,
        "is_vip": True,
        "memo": f"Master Transfer Authorization Flag: {FLAG}"
    },
    101: {
        "id": 101,
        "owner": "Alice Parker",
        "account_type": "Standard Checking",
        "balance": 250.50,
        "is_vip": False,
        "memo": "Monthly rent and utilities allowance."
    },
    102: {
        "id": 102,
        "owner": "Bob Miller",
        "account_type": "Personal Savings",
        "balance": 1200.00,
        "is_vip": False,
        "memo": "Vehicle emergency fund."
    }
}

HTML_LAYOUT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Apex Global Bank - Private Client Portal</title>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;800&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-dark: #070c18;
            --card-bg: #0f172a;
            --border: #1e293b;
            --accent: #10b981;
            --accent-glow: rgba(16, 185, 129, 0.25);
            --text-main: #f8fafc;
            --text-dim: #94a3b8;
            --danger: #ef4444;
            --gold: #fbbf24;
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
            background: rgba(15, 23, 42, 0.9);
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
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(251, 191, 36, 0.05));
            border: 1px solid var(--accent);
            padding: 1rem 1.5rem;
            border-radius: 8px;
            margin-bottom: 1.5rem;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
        }
        .balance-box {
            background: #050a14;
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 1.5rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: 1.25rem 0;
        }
        .amount {
            font-family: 'JetBrains Mono', monospace;
            font-size: 2rem;
            font-weight: 800;
            color: var(--accent);
        }
        .vip-amount { color: var(--gold); }
        .memo-box {
            background: #020617;
            border-left: 4px solid var(--accent);
            padding: 1rem;
            border-radius: 0 8px 8px 0;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.9rem;
            color: #38bdf8;
            word-break: break-all;
        }
        .hints-box {
            background: #090e1a;
            border-left: 4px solid var(--gold);
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
            <span>🏦</span> APEX GLOBAL BANK // IDOR LAB
        </div>
        <div style="font-size: 0.85rem; color: var(--text-dim); font-family: 'JetBrains Mono', monospace;">
            OWASP Top 10: A01 Broken Access Control / BOLA
        </div>
    </header>
    <div class="container">
        <div class="banner-challenge">
            <span>🎯 OBJECTIVE:</span> You are currently logged in as <strong>Alice Parker</strong> (Account ID: <code>101</code>). Manipulate object identifiers in the URL or API endpoints to view the confidential Executive Vault (Account ID: <code>1</code>) and extract the wire transfer flag!
        </div>
        {{ content | safe }}
    </div>
    <footer>
        Cybersecurity Training Lab Environment • CTF Challenge: Insecure Direct Object Reference (IDOR)
    </footer>
</body>
</html>
"""

@app.route('/')
def root():
    return redirect('/account?id=101')

@app.route('/account')
def account():
    account_id = request.args.get('id', '101')
    try:
        acc_num = int(account_id)
    except:
        acc_num = 101

    acc = ACCOUNTS.get(acc_num)
    if not acc:
        content = f"<div class='card'><h3 style='color:#ef4444;'>Account ID #{account_id} not found.</h3></div>"
        return render_template_string(HTML_LAYOUT, content=content)

    is_vip = acc.get("is_vip", False)

    content = f"""
    <div class="card">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 1rem;">
            <div>
                <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; color: var(--text-dim);">ACCOUNT NUMBER: #{acc['id']}</span>
                <h2 style="color: #fff; margin-top: 0.25rem;">{acc['owner']}</h2>
                <p style="color: var(--text-dim); font-size: 0.9rem;">{acc['account_type']}</p>
            </div>
            <div>
                <span style="background: {'rgba(251,191,36,0.2)' if is_vip else 'rgba(16,185,129,0.2)'}; border: 1px solid {'#fbbf24' if is_vip else '#10b981'}; color: {'#fde68a' if is_vip else '#6ee7b7'}; padding: 0.35rem 0.8rem; border-radius: 6px; font-weight: 700; font-size: 0.85rem;">
                    {'👑 VIP EXECUTIVE' if is_vip else 'STANDARD USER'}
                </span>
            </div>
        </div>

        <div class="balance-box">
            <div>
                <span style="font-size: 0.85rem; color: var(--text-dim);">AVAILABLE BALANCE</span>
                <div class="amount {'vip-amount' if is_vip else ''}">${acc['balance']:,.2f}</div>
            </div>
            <div style="text-align: right;">
                <span style="font-size: 0.85rem; color: var(--text-dim);">STATUS</span>
                <div style="color: #10b981; font-weight: bold; font-family: 'JetBrains Mono', monospace;">ACTIVE / VERIFIED</div>
            </div>
        </div>

        <h4 style="color: #fff; margin-bottom: 0.5rem;">Confidential Account Notes & Wire Memo:</h4>
        <div class="memo-box">
            {acc['memo']}
        </div>

        <div class="hints-box">
            <strong>💡 IDOR Exploit Parameter:</strong>
            <p style="margin-top: 0.35rem;">Observe the query parameter in your address bar: <code>/account?id=101</code>. Try inspecting other IDs like <code>?id=1</code> or <code>?id=102</code>.</p>
            <p style="margin-top: 0.35rem;">REST API endpoint: <a href="/api/account/{acc['id']}" target="_blank" style="color: var(--gold);">/api/account/{acc['id']}</a></p>
        </div>
    </div>
    """
    return render_template_string(HTML_LAYOUT, content=content)

@app.route('/api/account/<int:account_id>')
def api_account(account_id):
    # VULNERABILITY: BOLA / IDOR on API route without session verification
    acc = ACCOUNTS.get(account_id)
    if acc:
        return jsonify(acc)
    return jsonify({"error": "Account not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
