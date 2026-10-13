from flask import Flask, request, render_template_string
import os
from lxml import etree

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "CTF{xx3_3xt3rn4l_3nt1ty_xpl01t_9912}")

# Write flag to system
with open("/flag.txt", "w") as f:
    f.write(FLAG + "\n")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Enterprise XML Invoicer // XXE Security Lab</title>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;800&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg: #0b0f19;
            --card: #131b2e;
            --border: #1e293b;
            --accent: #f59e0b;
            --accent-glow: rgba(245, 158, 11, 0.25);
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
            background: rgba(19, 27, 46, 0.9);
            border-bottom: 1px solid var(--border);
            padding: 1.25rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .brand {
            font-family: 'JetBrains Mono', monospace;
            font-size: 1.25rem;
            font-weight: 800;
            color: var(--accent);
        }
        .container {
            max-width: 950px;
            margin: 2rem auto;
            padding: 0 1rem;
            flex: 1;
            width: 100%;
        }
        .card {
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 15px 35px -10px rgba(0,0,0,0.5);
        }
        .banner {
            background: linear-gradient(135deg, rgba(245, 158, 11, 0.1), rgba(234, 88, 12, 0.05));
            border: 1px solid var(--accent);
            padding: 1rem 1.5rem;
            border-radius: 8px;
            margin-bottom: 1.5rem;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
        }
        textarea {
            width: 100%;
            height: 180px;
            background: #060913;
            border: 1px solid var(--border);
            border-radius: 8px;
            color: #38bdf8;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
            padding: 1rem;
            resize: vertical;
        }
        textarea:focus { outline: none; border-color: var(--accent); box-shadow: 0 0 12px var(--accent-glow); }
        button {
            margin-top: 1rem;
            background: var(--accent);
            color: #000;
            font-weight: 700;
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            border: none;
            cursor: pointer;
            transition: all 0.2s;
        }
        button:hover { transform: translateY(-2px); box-shadow: 0 5px 18px var(--accent-glow); }
        .result-box {
            background: #040711;
            padding: 1.25rem;
            border-radius: 8px;
            border: 1px solid #1e293b;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
            color: #a7f3d0;
            white-space: pre-wrap;
            margin-top: 1.5rem;
        }
        .sample-box {
            background: #080d1a;
            border: 1px dashed var(--border);
            border-radius: 8px;
            padding: 1rem;
            margin-top: 1rem;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.8rem;
            color: var(--text-dim);
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
        <div class="brand">📑 XML INVOICER // XXE LAB</div>
        <div style="font-size: 0.85rem; color: var(--text-dim); font-family: 'JetBrains Mono', monospace;">OWASP Top 10: A05 Security Misconfiguration (XXE)</div>
    </header>
    <div class="container">
        <div class="banner">
            <span>🎯 OBJECTIVE:</span> The XML Invoice processor resolves external DTD entities. Craft an XXE payload to exfiltrate <code>/flag.txt</code> or <code>/etc/passwd</code>!
        </div>

        <div class="card">
            <h2 style="margin-bottom: 0.5rem;">Submit XML Invoice Payload</h2>
            <p style="color: var(--text-dim); margin-bottom: 1.25rem;">Enter your B2B purchase order or invoice XML data below for automated parsing.</p>

            <form method="POST" action="/parse">
                <textarea name="xml_data">{{ xml_input or default_xml }}</textarea>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <button type="submit">Parse Invoice XML 🚀</button>
                </div>
            </form>

            {% if error %}
                <div class="result-box" style="color: #ef4444; border-color: rgba(239, 68, 68, 0.4);">
                    <strong>Parsing Error:</strong> {{ error }}
                </div>
            {% endif %}

            {% if parsed_result %}
                <div class="result-box">
                    <strong>Parsed Invoice Output:</strong><br>
                    {{ parsed_result }}
                </div>
            {% endif %}

            <div class="sample-box">
                <strong>💡 Standard XML Format Example:</strong>
                <pre style="margin-top: 0.5rem; color: #94a3b8;">&lt;invoice&gt;
    &lt;customer&gt;ACME Corp&lt;/customer&gt;
    &lt;item&gt;Security Assessment License&lt;/item&gt;
    &lt;amount&gt;5000&lt;/amount&gt;
&lt;/invoice&gt;</pre>
            </div>
        </div>
    </div>
    <footer>
        Cybersecurity Training Lab Environment • CTF Challenge: XML External Entity (XXE)
    </footer>
</body>
</html>
"""

DEFAULT_XML = """<?xml version="1.0" encoding="UTF-8"?>
<invoice>
    <customer>CyberSec Corp</customer>
    <item>Hardware Security Module</item>
    <amount>12500</amount>
</invoice>"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, default_xml=DEFAULT_XML, xml_input=None, parsed_result=None, error=None)

@app.route('/parse', methods=['POST'])
def parse():
    xml_data = request.form.get('xml_data', '')
    if not xml_data:
        return render_template_string(HTML_TEMPLATE, default_xml=DEFAULT_XML, xml_input="", parsed_result=None, error="Empty XML input")
    
    try:
        # VULNERABILITY: resolve_entities=True allows XXE injection
        parser = etree.XMLParser(resolve_entities=True, load_dtd=True, no_network=False)
        root = etree.fromstring(xml_data.encode('utf-8'), parser=parser)
        
        customer = root.findtext('customer') or "N/A"
        item = root.findtext('item') or "N/A"
        amount = root.findtext('amount') or "N/A"
        
        output = f"Customer / Entity: {customer}\nItem: {item}\nAmount: ${amount}"
        return render_template_string(HTML_TEMPLATE, default_xml=DEFAULT_XML, xml_input=xml_data, parsed_result=output, error=None)
    except Exception as e:
        return render_template_string(HTML_TEMPLATE, default_xml=DEFAULT_XML, xml_input=xml_data, parsed_result=None, error=str(e))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
