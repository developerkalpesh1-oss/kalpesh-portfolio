#!/usr/bin/env python3
"""
WSGI entrypoint named `app` so deployment/runtime detects it.
Provides a minimal health-check WSGI app and, when run directly,
starts the project's existing static file server.
"""
from wsgiref.simple_server import make_server

# Import the project's existing run() so running this file still serves files
try:
    from server import run as _run  # server.py in project root
except Exception:
    _run = None

def app(environ, start_response):
    """Minimal WSGI app required by many hosting platforms."""
    status = "200 OK"
    headers = [("Content-Type", "text/plain; charset=utf-8")]
    start_response(status, headers)
    return [b"OK"]

if __name__ == "__main__":
    # If the original server.run is available, use it to serve the project files.
    if _run:
        _run(8000)
    else:
        # Fallback: run a simple WSGI server that responds to health checks.
        print("Starting minimal WSGI health-check server on http://0.0.0.0:8000/")
        make_server("0.0.0.0", 8000, app).serve_forever()

