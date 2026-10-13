from flask import Flask, request, render_template_string, jsonify
from flask_sock import Sock
import os
import json
import time
import threading

app = Flask(__name__)
sock = Sock(app)

FLAG = os.environ.get("FLAG", "CTF{csw5h_w3bs0ck3t_h1j4ck_0r1g1n_pwn_5512}")

CLIENTS = set()

def admin_broadcaster():
    """Simulates internal system messages sent to connected WebSocket clients."""
    time.sleep(2)
    while True:
        try:
            msg = {
                "sender": "System Daemon (Admin)",
                "timestamp": time.strftime("%H:%M:%S"),
                "channel": "confidential-sec-ops",
                "message": f"🔒 SYSTEM SECURITY AUDIT: Operational token verified: {FLAG}"
            }
            payload = json.dumps(msg)
            dead_clients = set()
            for ws in list(CLIENTS):
                try:
                    ws.send(payload)
                except Exception:
                    dead_clients.add(ws)
            for dc in dead_clients:
                CLIENTS.discard(dc)
        except Exception:
            pass
        time.sleep(5)

# Start background broadcast thread
threading.Thread(target=admin_broadcaster, daemon=True).start()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Aether Ops // WebSocket Security Lab</title>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;800&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg: #070b14;
            --card: #0f172a;
            --border: #1e293b;
            --accent: #06b6d4;
            --accent-glow: rgba(6, 182, 212, 0.25);
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
            background: rgba(15, 23, 42, 0.95);
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
            background: linear-gradient(135deg, rgba(6, 182, 212, 0.1), rgba(8, 145, 178, 0.05));
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
        .chat-box {
            background: #030712;
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 1rem;
            height: 250px;
            overflow-y: auto;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.8rem;
            margin-bottom: 1rem;
        }
        .chat-msg { margin-bottom: 0.6rem; line-height: 1.4; }
        .chat-sender { color: #38bdf8; font-weight: 700; }
        .chat-admin { color: #f43f5e; font-weight: 700; }
        .chat-text { color: #e2e8f0; }
        input {
            width: 100%;
            background: #060913;
            border: 1px solid var(--border);
            border-radius: 8px;
            color: #38bdf8;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
            padding: 0.75rem;
            margin-bottom: 0.75rem;
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
        }
        button:hover { transform: translateY(-2px); box-shadow: 0 5px 15px var(--accent-glow); }
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
        <div class="brand">💬 AETHER OPS // WEBSOCKET HIJACKING (CSWSH)</div>
        <div style="font-size: 0.85rem; color: var(--text-dim); font-family: 'JetBrains Mono', monospace;">OWASP A01: Cross-Site WebSocket Hijacking</div>
    </header>

    <div class="container">
        <div class="banner">
            🎯 <strong>MISSION:</strong> The WebSocket handshake at <code>/ws</code> lacks Origin validation.<br>
            • Connect to the live WebSocket feed or simulate an external origin hijack from <code>http://evil-tracker.com</code>.<br>
            • Intercept the live broadcast stream emitted by the automated admin bot to extract the confidential security audit flag!
        </div>

        <div class="grid">
            <!-- Live Chat Client -->
            <div class="card">
                <h2>📡 Live Operations Channel</h2>
                <div class="chat-box" id="liveChat"></div>
                <input type="text" id="chatInput" placeholder="Type a broadcast message..." onkeydown="if(event.key==='Enter') sendMsg()">
                <button onclick="sendMsg()">Send Message 📤</button>
            </div>

            <!-- Attacker CSWSH Workbench -->
            <div class="card">
                <h2>🏴‍☠️ Attacker CSWSH Hijack Workbench</h2>
                <p style="color: var(--text-dim); font-size: 0.85rem; margin-bottom: 0.75rem;">
                    Test establishing a WebSocket connection from an unauthorized origin with standard JavaScript <code>new WebSocket()</code>:
                </p>
                <div class="chat-box" id="hijackLog" style="height: 200px; color: #a7f3d0;">
                    // Hijacked WebSocket stream:
                </div>
                <button onclick="startHijackStream()" style="background: #ec4899; color: #fff;">Start Intercept Stream 🛰️</button>
            </div>
        </div>
    </div>

    <footer>
        CyberSec Range • Cross-Site WebSocket Hijacking (CSWSH) Challenge
    </footer>

    <script>
        let ws;
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = protocol + '//' + window.location.host + '/ws';

        function connect() {
            ws = new WebSocket(wsUrl);
            ws.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    const chat = document.getElementById('liveChat');
                    const div = document.createElement('div');
                    div.className = 'chat-msg';
                    
                    const isAdmin = data.sender.includes('Admin') || data.sender.includes('Daemon');
                    div.innerHTML = `<span class="${isAdmin ? 'chat-admin' : 'chat-sender'}">[${data.timestamp}] ${data.sender}:</span> <span class="chat-text">${data.message}</span>`;
                    chat.appendChild(div);
                    chat.scrollTop = chat.scrollHeight;
                } catch(e) {}
            };
        }

        function sendMsg() {
            const input = document.getElementById('chatInput');
            if(input.value && ws && ws.readyState === WebSocket.OPEN) {
                const payload = {
                    sender: "Analyst_Operator",
                    timestamp: new Date().toLocaleTimeString(),
                    message: input.value
                };
                ws.send(JSON.stringify(payload));
                input.value = '';
            }
        }

        function startHijackStream() {
            const log = document.getElementById('hijackLog');
            log.textContent = '[*] Opening cross-origin WebSocket connection to ' + wsUrl + '...\\n';
            const evilWs = new WebSocket(wsUrl);
            evilWs.onopen = () => {
                log.textContent += '[+] WebSocket Handshake ACCEPTED (No Origin Check!)\\n[*] Listening for confidential admin broadcasts...\\n\\n';
            };
            evilWs.onmessage = (event) => {
                log.textContent += '[INTERCEPTED] ' + event.data + '\\n';
                log.scrollTop = log.scrollHeight;
            };
        }

        connect();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@sock.route('/ws')
def chat_ws(ws):
    # VULNERABILITY: No Origin header validation in handshake!
    CLIENTS.add(ws)
    try:
        # Welcome message
        welcome = {
            "sender": "System Gateway",
            "timestamp": time.strftime("%H:%M:%S"),
            "message": "Connected to Aether Operations WebSocket room."
        }
        ws.send(json.dumps(welcome))
        
        while True:
            data = ws.receive()
            if data is None:
                break
            try:
                msg_obj = json.loads(data)
                # Broadcast user message to all clients
                dead = set()
                for client in list(CLIENTS):
                    try:
                        client.send(json.dumps(msg_obj))
                    except Exception:
                        dead.add(client)
                for d in dead:
                    CLIENTS.discard(d)
            except Exception:
                pass
    finally:
        CLIENTS.discard(ws)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
