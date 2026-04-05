#!/usr/bin/env python3
"""
WSGI entrypoint named `app` so deployment/runtime detects it.
Includes the project's static file server (moved from server.py) and
provides a minimal health-check WSGI app for hosting platforms.
"""
import http.server
import socketserver
import webbrowser
import os
import sys
from wsgiref.simple_server import make_server

PORT = 8000

here = os.path.dirname(os.path.abspath(__file__))
os.chdir(here)

Handler = http.server.SimpleHTTPRequestHandler

def run(port=PORT):
    with socketserver.TCPServer(("127.0.0.1", port), Handler) as httpd:
        url = f"http://127.0.0.1:{port}/"
        print(f"Serving {here} at {url}")
        try:
            webbrowser.open(url)
        except Exception:
            pass
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server")

def app(environ, start_response):
    """Minimal WSGI app required by many hosting platforms."""
    status = "200 OK"
    headers = [("Content-Type", "text/plain; charset=utf-8")]
    start_response(status, headers)
    return [b"OK"]

if __name__ == "__main__":
    port = PORT
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            pass
    # Prefer serving static files via run()
    try:
        run(port)
    except Exception:
        print("Falling back to minimal WSGI server on 0.0.0.0:8000")
        make_server("0.0.0.0", 8000, app).serve_forever()

