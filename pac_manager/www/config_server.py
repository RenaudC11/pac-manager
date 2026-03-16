#!/usr/bin/env python3
"""Serveur HTTP minimal pour persister la config PAC Manager dans /data/"""
import http.server, json, os, sys

CONFIG_FILE = '/data/pac_config.json'

class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, fmt, *args): pass  # Silencieux

    def do_OPTIONS(self):
        self.send_response(200)
        self._cors()
        self.end_headers()

    def do_GET(self):
        if self.path != '/pac-config':
            self.send_response(404); self.end_headers(); return
        try:
            with open(CONFIG_FILE, 'r') as f:
                data = f.read()
            self.send_response(200)
            self._cors()
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(data.encode())
        except FileNotFoundError:
            self.send_response(404)
            self._cors()
            self.end_headers()
            self.wfile.write(b'{}')

    def do_POST(self):
        if self.path != '/pac-config':
            self.send_response(404); self.end_headers(); return
        try:
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length)
            # Valider le JSON avant d'écrire
            json.loads(body)
            with open(CONFIG_FILE, 'w') as f:
                f.write(body.decode())
            self.send_response(200)
            self._cors()
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"ok":true}')
        except Exception as e:
            self.send_response(500)
            self._cors()
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())

    def _cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

if __name__ == '__main__':
    server = http.server.HTTPServer(('127.0.0.1', 8098), Handler)
    print('[config_server] Démarré sur 127.0.0.1:8098')
    server.serve_forever()
