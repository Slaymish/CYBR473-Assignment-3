# client_stub.py
import uuid, time, requests, os, crypto
CID = str(uuid.uuid4())
HEAD = {"X-API-KEY": os.getenv("C2_SECRET", "changeme")}
BASE = "http://localhost:5000"

def beacon():
    requests.post(f"{BASE}/register", headers=HEAD, json={"id": CID})
    while True:
        cmd = requests.get(f"{BASE}/command?id={CID}", headers=HEAD).json()["cmd"]
        if cmd == "pwn":
            print("popping messagebox (stub)…")
        elif cmd.startswith("slp"):
            time.sleep(int(cmd.split()[1]))
        time.sleep(10)

if __name__ == "__main__":
    beacon()

