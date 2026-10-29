"""Offline server."""
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
import json,webbrowser
from .main import compile_source
ROOT=Path(__file__).resolve().parents[1]
class Handler(SimpleHTTPRequestHandler):
 def __init__(self,*a,**kw):super().__init__(*a,directory=str(ROOT/'web'),**kw)
 def do_GET(self):
  if self.path=='/api/examples':return self.json({p.stem:p.read_text() for p in sorted((ROOT/'examples').glob('*.tc'))})
  if self.path=='/api/docs':return self.json({'source':(ROOT/'web'/'docs-data.js').read_text()})
  return super().do_GET()
 def do_POST(self):
  if self.path!='/api/compile':self.send_error(404);return
  self.json(compile_source(json.loads(self.rfile.read(int(self.headers.get('Content-Length','0')))).get('source','')))
 def json(self,o):
  b=json.dumps(o).encode();self.send_response(200);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(b)));self.end_headers();self.wfile.write(b)
 def log_message(self,*a):pass
def serve(port=8000):
 for candidate in range(port, min(port + 20, 65536)):
  try:s=ThreadingHTTPServer(('127.0.0.1',candidate),Handler);break
  except OSError:s=None
 if s is None:
  s=ThreadingHTTPServer(('127.0.0.1',0),Handler)
 port=s.server_address[1]
 print(f'TinyC Studio: http://127.0.0.1:{port}');webbrowser.open(f'http://127.0.0.1:{port}');s.serve_forever()
