from flask import Flask, request, render_template_string
import subprocess
import os

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "CTF{0s_c0mm4nd_1nj3ct10n_p1ng_pwn3d_4421}")

# Write flag to hidden file
with open('/root/flag.txt', 'w') as f:
    f.write(FLAG + "\n")
with open('/etc/secret_ctf_flag.conf', 'w') as f:
    f.write(f"SYSTEM_INTEGRITY_FLAG={FLAG}\n")

HTML_LAYOUT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NetProbe - Network Diagnostics & Ping Utility</title>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;800&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-dark: #080c14;
            --card-bg: #101726;
            --border: #1d273b;
            --accent: #10b981;
            --accent-glow: rgba(16, 185, 129, 0.25);
            --text-main: #f8fafc;
            --text-dim: #94a3b8;
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
            background: rgba(16, 23, 38, 0.9);
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
            box-shadow: 0 15px 35px -10px rgba(0,0,0,0.6);
            margin-bottom: 2rem;
        }
        .banner-challenge {
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(6, 182, 212, 0.05));
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
            background: #070c16;
            color: #fff;
            font-family: inherit;
            font-size: 0.95rem;
        }
        input:focus { outline: none; border-color: var(--accent); box-shadow: 0 0 12px var(--accent-glow); }
        button {
            background: var(--accent);
            color: #041209;
            font-weight: 700;
            cursor: pointer;
            border: none;
            transition: all 0.2s;
        }
        button:hover { transform: translateY(-2px); box-shadow: 0 5px 18px var(--accent-glow); }
        .terminal-box {
            background: #030712;
            padding: 1.25rem;
            border-radius: 8px;
            border: 1px solid #1f2937;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
            color: #4ade80;
            white-space: pre-wrap;
            word-break: break-all;
            margin-top: 1rem;
            max-height: 400px;
            overflow-y: auto;
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
        .hints-box code { color: #38bdf8; font-family: 'JetBrains Mono', monospace; }
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
            <span>📡</span> NETPROBE // OS COMMAND INJECTION LAB
        </div>
        <div style="font-size: 0.85rem; color: var(--text-dim); font-family: 'JetBrains Mono', monospace;">
            OWASP Top 10: A03 Injection (Command Execution)
        </div>
    </header>
    <div class="container">
        <div class="banner-challenge">
            <span>🎯 OBJECTIVE:</span> Leverage command chaining operators (<code>;</code>, <code>&&</code>, <code>||</code>, <code>|</code>, or <code>`cmd`</code>) in the IP address field to bypass the ping utility and read the server secret in <code>/etc/secret_ctf_flag.conf</code> or <code>/root/flag.txt</code>!
        </div>

        <div class="card">
            <h2 style="color: #fff; margin-bottom: 0.5rem;">Host Reachability Diagnostic Utility</h2>
            <p style="color: var(--text-dim); margin-bottom: 1.5rem;">Send ICMP Echo requests to test network connectivity and round-trip latency.</p>
            
            <form method="POST" action="/" style="display: flex; gap: 1rem; flex-wrap: wrap;">
                <input type="text" name="host" placeholder="127.0.0.1 or 8.8.8.8" value="{{ host }}" style="flex: 1; min-width: 300px;" required>
                <button type="submit">Execute Ping Probe</button>
            </form>

            {% if output is not none %}
            <div style="margin-top: 2rem;">
                <h4 style="color: #fff; margin-bottom: 0.5rem;">Terminal Diagnostics Stream:</h4>
                <div class="terminal-box">{{ output }}</div>
            </div>
            {% endif %}

            <div class="hints-box">
                <strong>💡 Command Injection Payloads & Chaining Tricks:</strong>
                <ul style="margin-left: 1.5rem; margin-top: 0.5rem; line-height: 1.6;">
                    <li>List files: <code>127.0.0.1 ; ls -la /</code></li>
                    <li>Read flag config: <code>127.0.0.1 && cat /etc/secret_ctf_flag.conf</code></li>
                    <li>Environment inspect: <code>127.0.0.1 | env</code></li>
                    <li>Inline substitution: <code>`cat /etc/secret_ctf_flag.conf`</code></li>
                </ul>
            </div>
        </div>
    </div>
    <footer>
        Cybersecurity Training Lab Environment • CTF Challenge: Command Injection
    </footer>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    output = None
    host = request.form.get('host', '127.0.0.1') if request.method == 'POST' else ''
    
    if request.method == 'POST':
        # VULNERABILITY: shell=True with unescaped string formatting
        cmd = f"ping -c 2 {host}"
        try:
            res = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=8, text=True)
            output = res.stdout
        except subprocess.TimeoutExpired:
            output = "[Error: Command execution timed out]"
        except Exception as e:
            output = f"[Execution Error: {str(e)}]"
            
    return render_template_string(HTML_LAYOUT, host=host, output=output)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
