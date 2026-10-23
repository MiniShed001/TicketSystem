# -*- coding: utf-8 -*-
"""
TicketSystem H5 preview server with cache headers.
Usage: python preview_server.py  (run from deploy/ directory or anywhere)
Serves D:/TicketSystem/frontend/dist/build/h5 on port 8080.
- /assets/* (hashed filenames) -> long-term cache (immutable)
- index.html and others        -> no-cache (always fresh)
"""
import http.server
import socketserver
import os
import sys

PORT = int(os.environ.get("PREVIEW_PORT", "8080"))

_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(_HERE, "..", "frontend", "dist", "build", "h5"))


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def end_headers(self):
        path = self.path.split("?")[0]
        if path.startswith("/assets/"):
            # hashed asset: immutable long cache
            self.send_header("Cache-Control", "public, max-age=31536000, immutable")
        else:
            # html / others: no-cache so updates are picked up immediately
            self.send_header("Cache-Control", "no-cache")
        super().end_headers()

    def log_message(self, fmt, *args):
        sys.stdout.write("  [preview] %s\n" % (fmt % args))


def main():
    if not os.path.exists(os.path.join(ROOT, "index.html")):
        sys.stderr.write(
            "[preview] index.html not found. Build first: cd frontend && npm run build:h5\n"
        )
        sys.exit(1)
    with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
        sys.stdout.write("[preview] serving %s at http://127.0.0.1:%d\n" % (ROOT, PORT))
        sys.stdout.flush()
        httpd.serve_forever()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
