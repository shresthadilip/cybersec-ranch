from flask import Flask, request, render_template_string, send_from_directory, redirect, url_for
import os
import subprocess

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "CTF{f1l3_upl04d_lf1_rce_byp4ss_9934}")
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

with open('/flag.txt', 'w') as f:
    f.write(FLAG + "\n")

# Blacklist filter with bypass vulnerability
DISALLOWED_EXTENSIONS = ['.php', '.exe', '.sh', '.py']

HTML_LAYOUT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>MediaVault - File Manager & LFI Security Lab</title>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;800&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-dark: #080d1a;
            --card-bg: #111a2e;
            --border: #1e2c47;
            --accent: #ec4899;
            --accent-glow: rgba(236, 72, 153, 0.25);
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
            background: rgba(17, 26, 46, 0.9);
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
            margin-bottom: 2rem;
            box-shadow: 0 15px 35px -10px rgba(0,0,0,0.6);
        }
        .banner-challenge {
            background: linear-gradient(135deg, rgba(236, 72, 153, 0.1), rgba(168, 85, 247, 0.05));
            border: 1px solid var(--accent);
            padding: 1rem 1.5rem;
            border-radius: 8px;
            margin-bottom: 1.5rem;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
        }
        input, button {
            padding: 0.75rem 1rem;
            border-radius: 8px;
            border: 1px solid var(--border);
            background: #080c18;
            color: #fff;
            font-family: inherit;
            font-size: 0.95rem;
        }
        input:focus { outline: none; border-color: var(--accent); box-shadow: 0 0 12px var(--accent-glow); }
        button {
            background: var(--accent);
            color: #fff;
            font-weight: 700;
            cursor: pointer;
            border: none;
            transition: all 0.2s;
        }
        button:hover { transform: translateY(-2px); box-shadow: 0 5px 18px var(--accent-glow); }
        .output-box {
            background: #040711;
            padding: 1.25rem;
            border-radius: 8px;
            border: 1px solid #1e293b;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
            color: #f472b6;
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
            <span>📁</span> MEDIAVAULT // FILE UPLOAD & LFI LAB
        </div>
        <div style="font-size: 0.85rem; color: var(--text-dim); font-family: 'JetBrains Mono', monospace;">
            OWASP Top 10: A01 & A03 File Inclusion / Upload
        </div>
    </header>
    <div class="container">
        <div class="banner-challenge">
            <span>🎯 OBJECTIVE:</span> Exploit Local File Inclusion (LFI) via the template viewer OR upload an executable payload to read <code>/flag.txt</code> on the host system!
        </div>
        {{ content | safe }}
    </div>
    <footer>
        Cybersecurity Training Lab Environment • CTF Challenge: File Upload & LFI
    </footer>
</body>
</html>
"""

@app.route('/')
def index():
    page = request.args.get('page', '')
    page_content = None
    error = None
    
    if page:
        try:
            # VULNERABILITY: Local File Inclusion (No path traversal sanitization)
            file_path = os.path.join(os.path.dirname(__file__), 'pages', page) if not page.startswith('/') else page
            if os.path.exists(file_path):
                with open(file_path, 'r', errors='ignore') as f:
                    page_content = f.read()
            else:
                error = f"File '{file_path}' not found."
        except Exception as e:
            error = str(e)
            
    uploaded_files = os.listdir(UPLOAD_FOLDER)
    
    content = f"""
    <div class="card">
        <h2 style="color: #fff; margin-bottom: 0.5rem;">📄 Dynamic Document & Log Viewer (LFI Vector)</h2>
        <p style="color: var(--text-dim); margin-bottom: 1.25rem;">Load system help documents or audit logs dynamically.</p>
        
        <form method="GET" action="/" style="display: flex; gap: 1rem; flex-wrap: wrap;">
            <input type="text" name="page" placeholder="about.txt or /flag.txt or ../../../etc/passwd" value="{page}" style="flex: 1; min-width: 300px;" required>
            <button type="submit">Load Document</button>
        </form>

        {"<div class='output-box' style='color:#ef4444;'><strong>Error:</strong> " + error + "</div>" if error else ""}
        {"<div class='output-box'>" + page_content + "</div>" if page_content else ""}

        <div class="hints-box">
            <strong>💡 LFI Traversal Hints:</strong>
            <ul style="margin-left: 1.5rem; margin-top: 0.5rem; line-height: 1.6;">
                <li>Read System Users: <code>?page=/etc/passwd</code> or <code>?page=../../../../etc/passwd</code></li>
                <li>Read CTF Flag: <code>?page=/flag.txt</code></li>
                <li>Read Environment Variables: <code>?page=/proc/self/environ</code></li>
            </ul>
        </div>
    </div>

    <div class="card">
        <h2 style="color: #fff; margin-bottom: 0.5rem;">📤 Profile Media & Avatar Uploader</h2>
        <p style="color: var(--text-dim); margin-bottom: 1.25rem;">Upload custom avatars and documents (Restricted: .php, .exe, .sh, .py).</p>
        
        <form method="POST" action="/upload" enctype="multipart/form-data" style="display: flex; gap: 1rem; flex-wrap: wrap;">
            <input type="file" name="file" style="flex: 1;" required>
            <button type="submit">Upload File</button>
        </form>

        <h4 style="color: #fff; margin-top: 1.5rem; margin-bottom: 0.5rem;">Uploaded Media Files:</h4>
        <ul style="margin-left: 1.5rem; color: var(--text-dim);">
            {"".join([f"<li><a href='/uploads/{f}' target='_blank' style='color: var(--accent);'>{f}</a></li>" for f in uploaded_files]) if uploaded_files else "<li>No files uploaded yet.</li>"}
        </ul>
    </div>
    """
    return render_template_string(HTML_LAYOUT, content=content)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    if not file or file.filename == '':
        return redirect(url_for('index'))
    
    filename = file.filename
    ext = os.path.splitext(filename)[1].lower()
    
    if ext in DISALLOWED_EXTENSIONS:
        return f"<h3>Upload Blocked! Extension {ext} is restricted by security policy.</h3><a href='/'>Go back</a>", 403
    
    save_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(save_path)
    return redirect(url_for('index'))

@app.route('/uploads/<path:filename>')
def serve_upload(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    # Create sample page
    pages_dir = os.path.join(os.path.dirname(__file__), 'pages')
    os.makedirs(pages_dir, exist_ok=True)
    with open(os.path.join(pages_dir, 'about.txt'), 'w') as f:
        f.write("MediaVault Document Center v2.4\nAll rights reserved 2026.\n")
        
    app.run(host='0.0.0.0', port=5000, debug=False)
