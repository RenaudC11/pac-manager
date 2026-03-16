#!/usr/bin/env python3
"""Serveur HTTP minimal pour persister la config PAC Manager dans /data/"""
import http.server
import json
import os
import sys
import traceback

CONFIG_FILE = '/data/pac_config.json'

class Handler(http.server.BaseHTTPRequestHandler):

    def log_message(self, fmt, *args):
        # Activer les logs pour debug
        sys.stderr.write("[config_server] %s - %s\n" % (self.address_string(), fmt % args))
        sys.stderr.flush()

    def do_OPTIONS(self):
        self.send_response(200)
        self._cors()
        self.end_headers()

    def do_GET(self):
        sys.stderr.write("[config_server] GET %s\n" % self.path)
        sys.stderr.flush()
        if self.path != '/pac-config':
            self.send_response(404)
            self._cors()
            self.end_headers()
            self.wfile.write(b'Not found')
            return
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, 'r') as f:
                    data = f.read()
                sys.stderr.write("[config_server] GET OK — %d bytes\n" % len(data))
                self.send_response(200)
                self._cors()
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(data.encode())
            else:
                sys.stderr.write("[config_server] GET — fichier absent, retour vide\n")
                self.send_response(200)
                self._cors()
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(b'{}')
        except Exception as e:
            sys.stderr.write("[config_server] GET ERROR: %s\n" % traceback.format_exc())
            self.send_response(500)
            self._cors()
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())

    def do_POST(self):
        sys.stderr.write("[config_server] POST %s\n" % self.path)
        sys.stderr.flush()
        if self.path != '/pac-config':
            self.send_response(404)
            self._cors()
            self.end_headers()
            return
        try:
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length)
            sys.stderr.write("[config_server] POST body: %d bytes\n" % len(body))
            parsed = json.loads(body)
            # S'assurer que /data/ existe
            os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
            with open(CONFIG_FILE, 'w') as f:
                f.write(body.decode())
            sys.stderr.write("[config_server] POST OK — sauvegardé dans %s\n" % CONFIG_FILE)
            self.send_response(200)
            self._cors()
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"ok":true}')
        except Exception as e:
            sys.stderr.write("[config_server] POST ERROR: %s\n" % traceback.format_exc())
            self.send_response(500)
            self._cors()
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())

    def _cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

if __name__ == '__main__':
    sys.stderr.write("[config_server] Démarrage sur 127.0.0.1:8098\n")
    sys.stderr.write("[config_server] CONFIG_FILE = %s\n" % CONFIG_FILE)
    sys.stderr.write("[config_server] /data/ existe: %s\n" % os.path.exists('/data'))
    sys.stderr.write("[config_server] /data/ writable: %s\n" % os.access('/data', os.W_OK))
    sys.stderr.flush()
    try:
        server = http.server.HTTPServer(('127.0.0.1', 8098), Handler)
        sys.stderr.write("[config_server] Prêt sur 127.0.0.1:8098\n")
        sys.stderr.flush()
        server.serve_forever()
    except Exception as e:
        sys.stderr.write("[config_server] ERREUR FATALE: %s\n" % traceback.format_exc())
        sys.stderr.flush()
        sys.exit(1)
