import http.server
import socketserver
import os
import sys

PORT = int(os.environ.get("PORT", 8000))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.path.dirname(os.path.abspath(__file__)), **kwargs)
    
    def log_message(self, format, *args):
        # Clean logging
        sys.stderr.write(f"[DASHBOARD] {self.address_string()} - {format % args}\n")

if __name__ == '__main__':
    # Ensure UTF-8 output on Windows console
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("============================================================")
        print(f"[+] CyberSec Ranch Training Dashboard listening on port {PORT}")
        print(f"👉 Access UI: http://localhost:{PORT}")
        print("============================================================")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")

