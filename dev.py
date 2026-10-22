#!/usr/bin/env python3
"""Serve the People mockup locally and open the browser. No dependencies."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
import subprocess

site = Path(__file__).resolve().parent / 'site'
url = 'http://127.0.0.1:4173/'
handler = partial(SimpleHTTPRequestHandler, directory=str(site))

try:
    server = ThreadingHTTPServer(('127.0.0.1', 4173), handler)
except OSError as error:
    raise SystemExit(f'Could not start the dev server: {error}')

thread = Thread(target=server.serve_forever, daemon=True)
thread.start()
print(f'People mockup: {url}\nPress Ctrl+C to stop.', flush=True)
try:
    subprocess.run(['open', url], check=False)
    thread.join()
except KeyboardInterrupt:
    print('\nStopping the dev server.', flush=True)
finally:
    server.shutdown()
    server.server_close()
