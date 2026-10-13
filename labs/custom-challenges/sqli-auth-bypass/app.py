from flask import Flask, request, render_template_string, redirect, url_for, session, make_response
import sqlite3
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

FLAG = os.environ.get("FLAG", "CTF{5ql_1nj3ct10n_m4st3r_byp4ss_2026}")

def init_db():
    conn = sqlite3.connect('vulnerable_shop.db')
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS users')
    c.execute('DROP TABLE IF EXISTS secret_vault')
    c.execute('DROP TABLE IF EXISTS products')
    
    c.execute('''CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT,
        role TEXT
    )''')
    
    c.execute('''CREATE TABLE secret_vault (
        id INTEGER PRIMARY KEY,
        secret_name TEXT,
        secret_data TEXT
    )''')
    
    c.execute('''CREATE TABLE products (
        id INTEGER PRIMARY KEY,
        name TEXT,
        category TEXT,
        price REAL,
        description TEXT
    )''')
    
    c.execute("INSERT INTO users (username, password, role) VALUES ('admin', 'Sup3rS3cur3P4ssw0rd!#@992', 'administrator')")
    c.execute("INSERT INTO users (username, password, role) VALUES ('guest', 'guest', 'user')")
    c.execute("INSERT INTO users (username, password, role) VALUES ('alice', 'wonderland2026', 'user')")
    
    c.execute("INSERT INTO secret_vault (id, secret_name, secret_data) VALUES (1, 'Master System Flag', ?)", (FLAG,))
    c.execute("INSERT INTO secret_vault (id, secret_name, secret_data) VALUES (2, 'Root SSH Key', 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIExampleRootKeyOnly')")
    
    c.execute("INSERT INTO products VALUES (1, 'Cyber Defense Drone', 'hardware', 1299.99, 'Autonomous surveillance drone with encrypted telemetry.')")
    c.execute("INSERT INTO products VALUES (2, 'Hardware Security Module', 'hardware', 3499.00, 'FIPS 140-3 Level 4 certified cryptographic co-processor.')")
    c.execute("INSERT INTO products VALUES (3, 'Red Team Exploit Payload Kit', 'software', 499.50, 'Collection of penetration testing templates.')")
    c.execute("INSERT INTO products VALUES (4, 'Zero-Day Intelligence Feed', 'intelligence', 9999.00, 'Real-time threat feed subscription.')")
    
    conn.commit()
    conn.close()

HTML_LAYOUT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CyberSec Corp - Hardware & Intel Portal</title>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;800&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-dark: #090d16;
            --card-bg: #111827;
            --border: #1f293d;
            --accent: #00f0ff;
            --accent-glow: rgba(0, 240, 255, 0.2);
            --text-main: #e2e8f0;
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
            padding: 1rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: rgba(17, 24, 39, 0.8);
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
        nav a {
            color: var(--text-dim);
            text-decoration: none;
            margin-left: 1.5rem;
            font-size: 0.9rem;
            font-weight: 600;
            transition: color 0.2s;
        }
        nav a:hover, nav a.active { color: var(--accent); }
        .container {
            max-width: 1100px;
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
            box-shadow: 0 10px 30px -10px rgba(0,0,0,0.5);
        }
        .banner-challenge {
            background: linear-gradient(135deg, rgba(0,240,255,0.08), rgba(16,185,129,0.05));
            border: 1px solid var(--accent);
            padding: 1rem 1.5rem;
            border-radius: 8px;
            margin-bottom: 1.5rem;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
        }
        .banner-challenge span { color: var(--accent); font-weight: bold; }
        input, select, button {
            padding: 0.75rem 1rem;
            border-radius: 8px;
            border: 1px solid var(--border);
            background: #0d121f;
            color: #fff;
            font-family: inherit;
            font-size: 0.95rem;
        }
        input:focus { outline: none; border-color: var(--accent); box-shadow: 0 0 10px var(--accent-glow); }
        button {
            background: var(--accent);
            color: #000;
            font-weight: 700;
            cursor: pointer;
            border: none;
            transition: transform 0.15s, box-shadow 0.15s;
        }
        button:hover { transform: translateY(-2px); box-shadow: 0 5px 15px var(--accent-glow); }
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1.5rem; }
        .product-card {
            background: #0d1322;
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 1.25rem;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        .product-card h3 { color: #fff; font-size: 1.1rem; margin-bottom: 0.5rem; }
        .product-card .price { color: var(--success); font-family: 'JetBrains Mono', monospace; font-size: 1.15rem; font-weight: bold; margin-top: 1rem; }
        .product-card .category-tag {
            font-size: 0.75rem;
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
            background: rgba(0,240,255,0.1);
            color: var(--accent);
            display: inline-block;
            margin-bottom: 0.75rem;
        }
        .code-box {
            background: #040711;
            padding: 1rem;
            border-radius: 8px;
            border: 1px solid #1e293b;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
            color: #38bdf8;
            overflow-x: auto;
            margin-top: 1rem;
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
            <span>⚡</span> CYBERSEC LABS // SQLi CHALLENGE
        </div>
        <nav>
            <a href="/" {% if active == 'products' %}class="active"{% endif %}>Catalog Search</a>
            <a href="/login" {% if active == 'login' %}class="active"{% endif %}>Admin Portal</a>
            {% if session.get('user') %}
            <a href="/admin" {% if active == 'admin' %}class="active"{% endif %}>Vault Panel</a>
            <a href="/logout" style="color: var(--danger);">Logout ({{ session.get('user') }})</a>
            {% endif %}
        </nav>
    </header>
    <div class="container">
        <div class="banner-challenge">
            <span>🎯 OBJECTIVE:</span> Perform SQL Injection on the product catalog filter (UNION-based extraction) OR bypass administrative authentication to retrieve the flag stored in <code>secret_vault</code>!
        </div>
        {{ content | safe }}
    </div>
    <footer>
        Cybersecurity Training Lab Environment • CTF Challenge: SQL Injection & Data Exfiltration
    </footer>
</body>
</html>
"""

@app.route('/')
def index():
    category = request.args.get('category', '')
    query_display = ""
    error_msg = ""
    products = []
    
    conn = sqlite3.connect('vulnerable_shop.db')
    c = conn.cursor()
    
    if category:
        # VULNERABLE SQL QUERY (Direct String Concatenation)
        sql_query = f"SELECT id, name, category, price, description FROM products WHERE category = '{category}'"
        query_display = sql_query
        try:
            c.execute(sql_query)
            products = c.fetchall()
        except Exception as e:
            error_msg = str(e)
    else:
        sql_query = "SELECT id, name, category, price, description FROM products"
        query_display = sql_query
        c.execute(sql_query)
        products = c.fetchall()
    
    conn.close()

    content = f"""
    <div class="card">
        <h2 style="margin-bottom: 1rem; color: #fff;">Product Intelligence Catalog</h2>
        <p style="color: var(--text-dim); margin-bottom: 1.5rem;">Filter high-grade cybersecurity defense and penetration testing assets by category.</p>
        
        <form method="GET" action="/" style="display: flex; gap: 1rem; margin-bottom: 1.5rem; flex-wrap: wrap;">
            <input type="text" name="category" placeholder="e.g. hardware, software, or exploit payload" value="{category}" style="flex: 1; min-width: 250px;">
            <button type="submit">Filter Catalog</button>
            <a href="/" style="display: inline-flex; align-items: center; text-decoration: none; color: var(--text-dim); padding: 0.75rem 1rem;">Reset</a>
        </form>

        <div style="margin-bottom: 1.5rem;">
            <span style="font-size: 0.85rem; color: var(--text-dim);">Executed SQL Query (Debug View):</span>
            <div class="code-box">{query_display}</div>
        </div>

        {"<div class='alert alert-error'><strong>Database Error:</strong> " + error_msg + "</div>" if error_msg else ""}

        <div class="grid">
    """
    for p in products:
        p_name = p[1] if len(p) > 1 else 'N/A'
        p_cat = p[2] if len(p) > 2 else 'N/A'
        p_price = p[3] if len(p) > 3 else '0.00'
        p_desc = p[4] if len(p) > 4 else ''
        content += f"""
            <div class="product-card">
                <div>
                    <span class="category-tag">{p_cat}</span>
                    <h3>{p_name}</h3>
                    <p style="color: var(--text-dim); font-size: 0.85rem; margin-top: 0.5rem;">{p_desc}</p>
                </div>
                <div class="price">${p_price}</div>
            </div>
        """
    content += "</div></div>"
    
    return render_template_string(HTML_LAYOUT, content=content, active='products', session=session)

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ""
    error = ""
    debug_query = ""
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        
        conn = sqlite3.connect('vulnerable_shop.db')
        c = conn.cursor()
        
        # VULNERABLE SQL QUERY (Auth Bypass via SQLi)
        query = f"SELECT id, username, role FROM users WHERE username = '{username}' AND password = '{password}'"
        debug_query = query
        try:
            c.execute(query)
            user = c.fetchone()
            if user:
                session['user'] = user[1]
                session['role'] = user[2]
                conn.close()
                return redirect(url_for('admin'))
            else:
                error = "Invalid credentials. Try SQL injection auth bypass payload!"
        except Exception as e:
            error = f"SQL Execution Error: {str(e)}"
        conn.close()

    content = f"""
    <div class="card" style="max-width: 500px; margin: 0 auto;">
        <h2 style="margin-bottom: 0.5rem; color: #fff;">Admin Authentication</h2>
        <p style="color: var(--text-dim); font-size: 0.9rem; margin-bottom: 1.5rem;">Restricted access to the CyberSec secret vault.</p>
        
        {"<div class='alert alert-error'>" + error + "</div>" if error else ""}
        
        <form method="POST" action="/login" style="display: flex; flex-direction: column; gap: 1rem;">
            <div>
                <label style="display: block; font-size: 0.85rem; margin-bottom: 0.35rem; color: var(--text-dim);">Username</label>
                <input type="text" name="username" placeholder="admin" style="width: 100%;" required>
            </div>
            <div>
                <label style="display: block; font-size: 0.85rem; margin-bottom: 0.35rem; color: var(--text-dim);">Password</label>
                <input type="password" name="password" placeholder="••••••••" style="width: 100%;">
            </div>
            <button type="submit" style="margin-top: 0.5rem;">Authenticate</button>
        </form>

        {f'<div class="code-box" style="margin-top: 1.5rem;"><strong>Query:</strong> {debug_query}</div>' if debug_query else ''}
    </div>
    """
    return render_template_string(HTML_LAYOUT, content=content, active='login', session=session)

@app.route('/admin')
def admin():
    if not session.get('user'):
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('vulnerable_shop.db')
    c = conn.cursor()
    c.execute("SELECT id, secret_name, secret_data FROM secret_vault")
    secrets = c.fetchall()
    conn.close()

    rows = ""
    for s in secrets:
        rows += f"""
        <tr style="border-bottom: 1px solid var(--border);">
            <td style="padding: 1rem; color: var(--accent);">{s[0]}</td>
            <td style="padding: 1rem; font-weight: 600;">{s[1]}</td>
            <td style="padding: 1rem; font-family: 'JetBrains Mono', monospace; color: #38bdf8; word-break: break-all;">{s[2]}</td>
        </tr>
        """

    content = f"""
    <div class="card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
            <div>
                <h2 style="color: #fff;">🔒 Encrypted Secret Vault</h2>
                <p style="color: var(--text-dim); font-size: 0.9rem;">Authenticated as: <strong style="color: var(--accent);">{session.get('user')}</strong> (Role: {session.get('role')})</p>
            </div>
            <div class="alert alert-success" style="margin: 0; padding: 0.5rem 1rem;">ACCESS GRANTED</div>
        </div>

        <table style="width: 100%; border-collapse: collapse; text-align: left; background: #070b14; border-radius: 8px; overflow: hidden;">
            <thead>
                <tr style="background: #0f172a; border-bottom: 1px solid var(--border); color: var(--text-dim); font-size: 0.85rem;">
                    <th style="padding: 1rem;">ID</th>
                    <th style="padding: 1rem;">Secret Identifier</th>
                    <th style="padding: 1rem;">Secret Payload / Flag</th>
                </tr>
            </thead>
            <tbody>
                {rows}
            </tbody>
        </table>
    </div>
    """
    return render_template_string(HTML_LAYOUT, content=content, active='admin', session=session)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=False)
