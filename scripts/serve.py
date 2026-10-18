"""Serve the prebuilt project locally, without installing Python packages.

Usage: python scripts/serve.py --open
Only loopback is bound. This is a read-only preview server, not a production backend.
"""
from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from functools import partial
import argparse,webbrowser

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port',type=int,default=8000)
    parser.add_argument('--open',action='store_true',help='Open the local URL in your default browser')
    args=parser.parse_args()
    root=Path(__file__).resolve().parents[1]
    try:server=ThreadingHTTPServer(('127.0.0.1',args.port),partial(SimpleHTTPRequestHandler,directory=str(root)))
    except OSError as error:parser.exit(1,f'Could not open port {args.port}: {error}\nTry --port 8001.\n')
    url=f'http://127.0.0.1:{server.server_port}/'
    print(f'NorthStar portfolio: {url}\nRead-only synthetic portfolio. Press Ctrl+C to stop.',flush=True)
    if args.open:webbrowser.open(url)
    try:server.serve_forever()
    except KeyboardInterrupt:pass
    finally:server.server_close()
if __name__=='__main__':main()
