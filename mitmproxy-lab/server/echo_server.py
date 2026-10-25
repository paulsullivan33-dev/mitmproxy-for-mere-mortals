#!/usr/bin/env python3
"""A throwaway echo server for the mitmproxy lab.

It answers every request with a plain-text report of what it
received: the method, the path, every header, and the body.
That makes changes a proxy (or an addon) makes to a request
visible in the response itself.

Usage:
    python3 echo_server.py [port]            # plain HTTP
    python3 echo_server.py [port] cert.pem key.pem   # HTTPS
"""

import ssl
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


class Echo(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def _answer(self):
        length = int(self.headers.get("Content-Length") or 0)
        body = self.rfile.read(length) if length else b""
        lines = [
            "served-by: plain-echo-server",
            f"method: {self.command}",
            f"path: {self.path}",
            "headers:",
        ]
        for name, value in self.headers.items():
            lines.append(f"  {name}: {value}")
        lines.append("body:")
        lines.append(body.decode("utf-8", "replace"))
        payload = ("\n".join(lines) + "\n").encode()
        status = 404 if self.path.startswith("/missing") else 200
        self.send_response(status)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    do_GET = _answer
    do_POST = _answer
    do_PUT = _answer
    do_DELETE = _answer

    def log_message(self, fmt, *args):  # keep the terminal quiet
        sys.stderr.write("echo-server: %s\n" % (fmt % args))


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 18080
    server = ThreadingHTTPServer(("127.0.0.1", port), Echo)
    if len(sys.argv) > 3:
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ctx.load_cert_chain(sys.argv[2], sys.argv[3])
        server.socket = ctx.wrap_socket(server.socket, server_side=True)
    print(f"echo-server listening on 127.0.0.1:{port}", flush=True)
    server.serve_forever()
