from flask import Flask, request, jsonify, render_template_string, session
import os
import time
import uuid

app = Flask(__name__)
app.secret_key = os.urandom(24)
FLAG = os.environ.get("FLAG", "CTF{r4c3_c0nd1t10n_t0ct0u_mult1thr34d_pwn3d_7719}")

# In-memory account store keyed by session ID
ACCOUNTS = {}

def get_account():
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
    uid = session['user_id']
    if uid not in ACCOUNTS:
        ACCOUNTS[uid] = {
            "balance": 50,
            "redeemed_coupons": set(),
            "inventory": []
        }
    return uid, ACCOUNTS[uid]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Race Condition Bank // Concurrency Exploit Arena</title>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;800&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg: #090e17;
            --card: #121927;
            --border: #1e2a3f;
            --accent: #eab308;
            --accent-glow: rgba(234, 179, 8, 0.25);
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
            background: linear-gradient(135deg, rgba(234, 179, 8, 0.1), rgba(161, 98, 7, 0.05));
            border: 1px solid var(--accent);
            padding: 1rem 1.5rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
            line-height: 1.5;
        }
        .balance-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: #0f172a;
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.5rem 2rem;
            margin-bottom: 1.5rem;
        }
        .balance-num {
            font-size: 2.2rem;
            font-weight: 800;
            color: #38bdf8;
            font-family: 'JetBrains Mono', monospace;
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
        input {
            width: 100%;
            background: #060913;
            border: 1px solid var(--border);
            border-radius: 8px;
            color: #facc15;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.9rem;
            padding: 0.75rem;
            margin-bottom: 1rem;
        }
        input:focus { outline: none; border-color: var(--accent); box-shadow: 0 0 10px var(--accent-glow); }
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
        .store-item {
            background: #0b111e;
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 1rem;
            margin-bottom: 0.75rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .log-box {
            margin-top: 1rem;
            background: #040711;
            border: 1px solid #1e293b;
            border-radius: 8px;
            padding: 1rem;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.8rem;
            color: #a7f3d0;
            min-height: 80px;
            max-height: 160px;
            overflow-y: auto;
            white-space: pre-wrap;
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
        <div class="brand">⚡ RACE CONDITION BANK // CONCURRENCY ARENA</div>
        <div style="font-size: 0.85rem; color: var(--text-dim); font-family: 'JetBrains Mono', monospace;">OWASP A04: Insecure Design & Concurrency Flaws</div>
    </header>

    <div class="container">
        <div class="banner">
            🎯 <strong>MISSION:</strong> You have an initial balance of $50. The VIP CTF Flag costs <strong>$1,000</strong> in the digital store.<br>
            A single-use promotional voucher <code>DISCOUNT2026</code> is valid for +$50.<br>
            Exploit the non-atomic check-then-act (TOCTOU) gap by firing parallel concurrent requests to redeem the coupon multiple times!
        </div>

        <div class="balance-header">
            <div>
                <div style="color: var(--text-dim); font-size: 0.85rem; text-transform: uppercase;">Your Wallet Balance</div>
                <div class="balance-num" id="balanceDisplay">${{ acc.balance }}</div>
            </div>
            <div>
                <button onclick="resetAccount()" style="background: #334155; color: #fff; width: auto; padding: 0.6rem 1.2rem;">Reset Session 🔄</button>
            </div>
        </div>

        <div class="grid">
            <!-- Coupon Redemption -->
            <div class="card">
                <h2>🎟️ Voucher Redemption</h2>
                <p style="color: var(--text-dim); font-size: 0.85rem; margin-bottom: 1rem;">Single-use coupon code: <code>DISCOUNT2026</code></p>
                <input type="text" id="couponCode" value="DISCOUNT2026">
                
                <button onclick="redeemCouponSingle()" style="margin-bottom: 0.75rem;">Redeem Voucher (Single Request)</button>
                
                <div style="background: #0a1120; border: 1px dashed #334155; border-radius: 8px; padding: 1rem; margin-top: 1rem;">
                    <div style="font-weight: 700; font-size: 0.85rem; margin-bottom: 0.5rem; color: #facc15;">🚀 In-Browser Concurrency Turbo Cannon</div>
                    <p style="font-size: 0.75rem; color: var(--text-dim); margin-bottom: 0.75rem;">Simultaneously dispatches 25 parallel asynchronous HTTP requests to trigger the TOCTOU window.</p>
                    <button onclick="blastParallelCoupons(25)" style="background: #ef4444; color: #fff;">Fire 25 Concurrent Requests! 💥</button>
                </div>
                
                <div class="log-box" id="couponLog">// Execution logs...</div>
            </div>

            <!-- Digital Store -->
            <div class="card">
                <h2>🛒 Digital Security Store</h2>
                <div class="store-item">
                    <div>
                        <div style="font-weight: 700;">Hacker Laptop Sticker</div>
                        <div style="color: var(--text-dim); font-size: 0.8rem;">$10.00</div>
                    </div>
                    <button onclick="buyItem('sticker')" style="width: auto; padding: 0.5rem 1rem;">Buy $10</button>
                </div>

                <div class="store-item">
                    <div>
                        <div style="font-weight: 700;">Dark Roast Coffee Pass</div>
                        <div style="color: var(--text-dim); font-size: 0.8rem;">$25.00</div>
                    </div>
                    <button onclick="buyItem('coffee')" style="width: auto; padding: 0.5rem 1rem;">Buy $25</button>
                </div>

                <div class="store-item" style="border-color: rgba(234, 179, 8, 0.4); background: #151a14;">
                    <div>
                        <div style="font-weight: 800; color: #facc15;">🚩 VIP CTF Master Flag</div>
                        <div style="color: var(--accent); font-size: 0.85rem; font-weight: 700;">$1,000.00</div>
                    </div>
                    <button onclick="buyItem('flag')" style="width: auto; padding: 0.5rem 1rem; background: #eab308; color: #000;">Buy $1,000</button>
                </div>

                <div class="log-box" id="storeLog">// Inventory & Purchases:
{% for item in acc.inventory %}
- Purchased: {{ item }}
{% endfor %}</div>
            </div>
        </div>
    </div>

    <footer>
        CyberSec Range • Race Condition & Concurrency Flaw CTF Arena
    </footer>

    <script>
        async function updateBalance() {
            const res = await fetch('/api/balance');
            const data = await res.json();
            document.getElementById('balanceDisplay').textContent = '$' + data.balance;
        }

        async function redeemCouponSingle() {
            const code = document.getElementById('couponCode').value;
            const log = document.getElementById('couponLog');
            log.textContent = 'Submitting voucher...';
            try {
                const res = await fetch('/api/redeem', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({code: code})
                });
                const data = await res.json();
                log.textContent = JSON.stringify(data, null, 2);
                updateBalance();
            } catch(e) {
                log.textContent = 'Error: ' + e.message;
            }
        }

        async function blastParallelCoupons(count) {
            const code = document.getElementById('couponCode').value;
            const log = document.getElementById('couponLog');
            log.textContent = `Firing ${count} parallel requests simultaneously...\n`;
            
            const promises = [];
            for (let i = 0; i < count; i++) {
                promises.push(
                    fetch('/api/redeem', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({code: code})
                    }).then(r => r.json())
                );
            }
            
            const results = await Promise.all(promises);
            let successes = results.filter(r => r.status === 'success').length;
            log.textContent = `Blast complete!\n- Total requests: ${count}\n- Successful redemptions: ${successes} / ${count}\n\nCheck your updated balance!`;
            updateBalance();
        }

        async function buyItem(item) {
            const log = document.getElementById('storeLog');
            log.textContent = 'Processing purchase...';
            try {
                const res = await fetch('/api/buy', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({item: item})
                });
                const data = await res.json();
                log.textContent = JSON.stringify(data, null, 2);
                updateBalance();
            } catch(e) {
                log.textContent = 'Error: ' + e.message;
            }
        }

        async function resetAccount() {
            await fetch('/api/reset', {method: 'POST'});
            location.reload();
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    uid, acc = get_account()
    return render_template_string(HTML_TEMPLATE, acc=acc)

@app.route('/api/balance')
def api_balance():
    uid, acc = get_account()
    return jsonify({"balance": acc["balance"]})

@app.route('/api/redeem', methods=['POST'])
def api_redeem():
    uid, acc = get_account()
    data = request.get_json(force=True) or {}
    code = data.get('code', '').strip().upper()

    if code != "DISCOUNT2026":
        return jsonify({"status": "error", "message": "Invalid voucher code"}), 400

    # VULNERABILITY: Check-Then-Act Concurrency Gap (TOCTOU)
    # Check
    if code in acc["redeemed_coupons"]:
        return jsonify({"status": "error", "message": "Voucher already redeemed for this account"}), 400

    # Deliberate micro-delay simulating database transaction lag
    time.sleep(0.08)

    # Act
    acc["balance"] += 50
    acc["redeemed_coupons"].add(code)

    return jsonify({
        "status": "success",
        "message": "Coupon redeemed! +$50 added to balance.",
        "current_balance": acc["balance"]
    }), 200

@app.route('/api/buy', methods=['POST'])
def api_buy():
    uid, acc = get_account()
    data = request.get_json(force=True) or {}
    item = data.get('item', '')

    catalog = {
        "sticker": {"name": "Hacker Laptop Sticker", "price": 10},
        "coffee": {"name": "Dark Roast Coffee Pass", "price": 25},
        "flag": {"name": "VIP CTF Master Flag", "price": 1000}
    }

    if item not in catalog:
        return jsonify({"status": "error", "message": "Unknown store item"}), 400

    target = catalog[item]
    if acc["balance"] < target["price"]:
        return jsonify({
            "status": "error",
            "message": f"Insufficient funds! You need ${target['price']} but only have ${acc['balance']}."
        }), 400

    acc["balance"] -= target["price"]
    
    if item == "flag":
        acc["inventory"].append(f"FLAG: {FLAG}")
        return jsonify({
            "status": "success",
            "message": "CONGRATULATIONS! You successfully purchased the Master CTF Flag!",
            "flag": FLAG,
            "balance": acc["balance"]
        }), 200
    else:
        acc["inventory"].append(target["name"])
        return jsonify({
            "status": "success",
            "message": f"Successfully purchased {target['name']}!",
            "balance": acc["balance"]
        }), 200

@app.route('/api/reset', methods=['POST'])
def api_reset():
    uid = session.get('user_id')
    if uid in ACCOUNTS:
        ACCOUNTS[uid] = {
            "balance": 50,
            "redeemed_coupons": set(),
            "inventory": []
        }
    return jsonify({"status": "success"})

if __name__ == '__main__':
    # Use threaded=True for concurrency handling
    app.run(host='0.0.0.0', port=5000, threaded=True, debug=False)
