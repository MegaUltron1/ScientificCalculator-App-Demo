"""Minimal local web server for the scientific calculator UI.

Serves static files from ./web and exposes a JSON API:
- POST /api/eval  {"expression": "..."}  -> {"value": 123.0} or {"error": "..."}
"""

from __future__ import annotations

import json
import pathlib
from http.server import BaseHTTPRequestHandler, HTTPServer

from calculator import CalculatorError, evaluate


WEB_DIR = pathlib.Path(__file__).with_name("web")


class Handler(BaseHTTPRequestHandler):
    def _send_json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_file(self, path: pathlib.Path) -> None:
        if not path.exists() or not path.is_file():
            self.send_error(404, "Not Found")
            return
        if path.suffix == ".html":
            ctype = "text/html; charset=utf-8"
        elif path.suffix == ".css":
            ctype = "text/css; charset=utf-8"
        elif path.suffix == ".js":
            ctype = "application/javascript; charset=utf-8"
        else:
            ctype = "application/octet-stream"
        data = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self) -> None:  # noqa: N802
        if self.path in ("/", "/index.html"):
            return self._send_file(WEB_DIR / "index.html")
        if self.path.startswith("/static/"):
            rel = self.path.removeprefix("/static/").lstrip("/").replace("/", "\\")
            return self._send_file(WEB_DIR / rel)
        self.send_error(404, "Not Found")

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/api/eval":
            self.send_error(404, "Not Found")
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            return self._send_json(400, {"error": "invalid Content-Length"})
        raw = self.rfile.read(length)
        try:
            payload = json.loads(raw.decode("utf-8"))
        except Exception:
            return self._send_json(400, {"error": "invalid JSON"})
        expr = payload.get("expression", "")
        try:
            result = evaluate(str(expr))
        except CalculatorError as e:
            return self._send_json(400, {"error": str(e)})
        return self._send_json(200, result.as_json())

    def log_message(self, fmt: str, *args) -> None:  # quieter logs
        return


def main() -> int:
    if not WEB_DIR.exists():
        raise SystemExit("Missing ./web directory")
    host, port = "127.0.0.1", 8000
    print(f"Serving on http://{host}:{port}")
    HTTPServer((host, port), Handler).serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

