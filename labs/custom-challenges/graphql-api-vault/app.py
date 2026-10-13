from flask import Flask, request, jsonify, render_template_string
import os

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "CTF{gr4phql_1ntr0sp3ct10n_s3cr3t_sch3m4_8819}")

# Mock DB
USERS = [
    {"id": 1, "username": "admin", "email": "admin@nexus-api.internal", "role": "SUPERADMIN", "isVerified": True},
    {"id": 2, "username": "alice", "email": "alice@nexus-api.internal", "role": "SECURITY_ENGINEER", "isVerified": True},
    {"id": 3, "username": "bob", "email": "bob@nexus-api.internal", "role": "USER", "isVerified": False}
]

SYSTEM_INFO = {
    "systemVersion": "v4.18.2-enterprise",
    "environment": "PRODUCTION",
    "debugMode": True,
    "maintenanceNotice": "Security audit in progress. Ensure introspection is disabled in production!"
}

SECRET_VAULT = {
    "vaultId": "VAULT-007-CLASSIFIED",
    "securityLevel": "TOP_SECRET",
    "masterPasscode": "nexus_shadow_protocol_2026",
    "confidentialFlag": FLAG
}

# Full GraphQL Introspection Schema Definition
INTROSPECTION_DATA = {
    "__schema": {
        "queryType": {"name": "Query"},
        "mutationType": {"name": "Mutation"},
        "types": [
            {
                "kind": "OBJECT",
                "name": "Query",
                "fields": [
                    {"name": "users", "description": "Returns list of public users", "args": [], "type": {"name": "UserList"}},
                    {"name": "user", "description": "Fetch user by ID", "args": [{"name": "id", "type": {"name": "Int"}}], "type": {"name": "User"}},
                    {"name": "systemConfig", "description": "System runtime metadata", "args": [], "type": {"name": "SystemConfig"}},
                    {"name": "vaultInspection", "description": "HIDDEN ADMIN VAULT - Inspect secret store credentials", "args": [{"name": "accessCode", "type": {"name": "String"}}], "type": {"name": "SecretVault"}}
                ]
            },
            {
                "kind": "OBJECT",
                "name": "Mutation",
                "fields": [
                    {"name": "unlockVaultFlag", "description": "Unlocks confidential flag with masterPasscode", "args": [{"name": "masterPasscode", "type": {"name": "String"}}], "type": {"name": "VaultResponse"}}
                ]
            },
            {
                "kind": "OBJECT",
                "name": "User",
                "fields": [
                    {"name": "id", "type": {"name": "Int"}},
                    {"name": "username", "type": {"name": "String"}},
                    {"name": "email", "type": {"name": "String"}},
                    {"name": "role", "type": {"name": "String"}},
                    {"name": "isVerified", "type": {"name": "Boolean"}}
                ]
            },
            {
                "kind": "OBJECT",
                "name": "SystemConfig",
                "fields": [
                    {"name": "systemVersion", "type": {"name": "String"}},
                    {"name": "environment", "type": {"name": "String"}},
                    {"name": "debugMode", "type": {"name": "Boolean"}},
                    {"name": "maintenanceNotice", "type": {"name": "String"}}
                ]
            },
            {
                "kind": "OBJECT",
                "name": "SecretVault",
                "fields": [
                    {"name": "vaultId", "type": {"name": "String"}},
                    {"name": "securityLevel", "type": {"name": "String"}},
                    {"name": "masterPasscode", "type": {"name": "String"}},
                    {"name": "confidentialFlag", "type": {"name": "String"}}
                ]
            }
        ]
    }
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GraphQL Vault // Introspection & API Security</title>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;800&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg: #090e17;
            --card: #121927;
            --border: #1e2a3f;
            --accent: #e11d48;
            --accent-glow: rgba(225, 29, 72, 0.25);
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
            background: linear-gradient(135deg, rgba(225, 29, 72, 0.1), rgba(159, 18, 57, 0.05));
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
        textarea {
            width: 100%;
            height: 240px;
            background: #060913;
            border: 1px solid var(--border);
            border-radius: 8px;
            color: #fb7185;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
            padding: 1rem;
            resize: vertical;
        }
        textarea:focus { outline: none; border-color: var(--accent); box-shadow: 0 0 10px var(--accent-glow); }
        button {
            width: 100%;
            background: var(--accent);
            color: #fff;
            font-weight: 700;
            padding: 0.75rem;
            border-radius: 8px;
            border: none;
            cursor: pointer;
            transition: all 0.2s;
            margin-top: 1rem;
        }
        button:hover { transform: translateY(-2px); box-shadow: 0 5px 15px var(--accent-glow); }
        .output {
            background: #030712;
            border: 1px solid #1f2937;
            border-radius: 8px;
            padding: 1rem;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.8rem;
            color: #a7f3d0;
            white-space: pre-wrap;
            word-break: break-all;
            height: 240px;
            overflow-y: auto;
        }
        .query-btn {
            background: #1e293b;
            color: #94a3b8;
            border: 1px solid var(--border);
            padding: 0.4rem 0.8rem;
            border-radius: 6px;
            font-size: 0.75rem;
            cursor: pointer;
            font-family: 'JetBrains Mono', monospace;
            margin-right: 0.5rem;
            margin-bottom: 0.5rem;
            display: inline-block;
        }
        .query-btn:hover { background: #334155; color: #fff; }
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
        <div class="brand">🔮 GRAPHQL VAULT // INTROSPECTION & MUTATION ARENA</div>
        <div style="font-size: 0.85rem; color: var(--text-dim); font-family: 'JetBrains Mono', monospace;">OWASP API Top 10: API Security</div>
    </header>

    <div class="container">
        <div class="banner">
            🎯 <strong>MISSION:</strong> Introspection is enabled on this GraphQL endpoint (<code>/graphql</code>).<br>
            • Run an introspection query (<code>{ __schema { types { name fields { name } } } }</code>) to discover hidden types and queries.<br>
            • Query the hidden <code>vaultInspection</code> object or execute the <code>unlockVaultFlag</code> mutation to retrieve the flag!
        </div>

        <div style="margin-bottom: 1rem;">
            <span style="color: var(--text-dim); font-size: 0.8rem; margin-right: 0.5rem;">Quick Payloads:</span>
            <span class="query-btn" onclick="setQuery('public')">Query Users</span>
            <span class="query-btn" onclick="setQuery('introspect')">Full Introspection</span>
            <span class="query-btn" onclick="setQuery('vault')">Vault Query</span>
            <span class="query-btn" onclick="setQuery('mutation')">Unlock Mutation</span>
        </div>

        <div class="grid">
            <div class="card">
                <h3 style="color: #fff; margin-bottom: 0.75rem;">GraphQL Query Editor</h3>
                <textarea id="graphqlQuery">{
  users {
    id
    username
    email
    role
  }
}</textarea>
                <button onclick="executeGraphQL()">Execute Query 🚀</button>
            </div>

            <div class="card">
                <h3 style="color: #fff; margin-bottom: 0.75rem;">JSON Response</h3>
                <div class="output" id="graphqlOutput">// Response will appear here...</div>
            </div>
        </div>
    </div>

    <footer>
        CyberSec Range • GraphQL Schema Introspection & Security Challenge
    </footer>

    <script>
        const queries = {
            public: `{\\n  users {\\n    id\\n    username\\n    email\\n    role\\n  }\\n}`,
            introspect: `{\\n  __schema {\\n    types {\\n      name\\n      fields {\\n        name\\n        description\\n      }\\n    }\\n  }\\n}`,
            vault: `{\\n  vaultInspection(accessCode: "ADMIN_DEBUG") {\\n    vaultId\\n    securityLevel\\n    masterPasscode\\n    confidentialFlag\\n  }\\n}`,
            mutation: `mutation {\\n  unlockVaultFlag(masterPasscode: "nexus_shadow_protocol_2026") {\\n    status\\n    flag\\n  }\\n}`
        };

        function setQuery(key) {
            document.getElementById('graphqlQuery').value = queries[key].replace(/\\\\n/g, '\\n');
        }

        async function executeGraphQL() {
            const query = document.getElementById('graphqlQuery').value;
            const out = document.getElementById('graphqlOutput');
            out.textContent = 'Executing query...';
            try {
                const res = await fetch('/graphql', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ query: query })
                });
                const data = await res.json();
                out.textContent = JSON.stringify(data, null, 2);
            } catch (err) {
                out.textContent = 'Error: ' + err.message;
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/graphql', methods=['POST', 'GET'])
def graphql_handler():
    if request.method == 'GET':
        query = request.args.get('query', '')
    else:
        data = request.get_json(force=True) or {}
        query = data.get('query', '')

    query = query.strip()

    if not query:
        return jsonify({"errors": [{"message": "Must provide query string."}]}), 400

    # Handle Schema Introspection
    if "__schema" in query:
        return jsonify({"data": INTROSPECTION_DATA})

    # Handle users query
    if "users" in query:
        return jsonify({"data": {"users": USERS}})

    # Handle systemConfig
    if "systemConfig" in query:
        return jsonify({"data": {"systemConfig": SYSTEM_INFO}})

    # Handle vaultInspection
    if "vaultInspection" in query:
        return jsonify({"data": {"vaultInspection": SECRET_VAULT}})

    # Handle mutation unlockVaultFlag
    if "unlockVaultFlag" in query:
        if "nexus_shadow_protocol_2026" in query:
            return jsonify({
                "data": {
                    "unlockVaultFlag": {
                        "status": "SUCCESS",
                        "message": "Passcode accepted. Vault decrypted!",
                        "flag": FLAG
                    }
                }
            })
        else:
            return jsonify({
                "data": {
                    "unlockVaultFlag": {
                        "status": "FAILED",
                        "message": "Invalid master passcode! Introspect the schema or inspect the vaultInspection query.",
                        "flag": None
                    }
                }
            })

    return jsonify({"errors": [{"message": f"Cannot query field '{query[:30]}...' on type 'Query'."}]}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
