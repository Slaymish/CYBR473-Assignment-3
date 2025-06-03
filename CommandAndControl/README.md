# Command & Control (C2) Server

This README tracks the **Core** and **Completion** requirements for the C2 server as described in the assignment brief.

---

## Core checklist

| Requirement                                                         | Status                                  |
| ------------------------------------------------------------------- | --------------------------------------- |
| Generate SQLite-backed registry of malware with unique ID, OS, arch | ✅ Implemented (`db.upsert_client`)      |
| `POST /register` endpoint for first‑time registration               | ✅                                       |
| `GET /command` polling endpoint returns one‑shot queued command     | ✅                                       |
| `POST /upload` accepts keylog payload & stores to disk + DB         | ✅                                       |
| `GET /clients` HTML list with ID, OS, arch, last‑seen               | ✅                                       |
| `GET /logs/<id>` view of decrypted keylogs                          | ✅                                       |
| `POST /commands` operator endpoint queues command                   | ✅                                       |
| Beacon tracking & active/inactive status (≤ 90 s sweeper)           | ✅ (`db.mark_stale` + background thread) |
| Data encoding/decoding helper (XOR + rotate‑right)                  | ✅ (`crypto.py`)                         |
| Shared secret auth on malware‑facing routes                         | ✅ (`require_secret` decorator)          |
| Persistent state (`c2.db`) survives restarts                        | ✅                                       |
| Unit test suite (pytest) with pre‑commit gate                       | ✅                                       |
| Makefile shortcuts (`make run`, `make test`)                        | ✅                                       |
| HTTPS support (adhoc cert)                                          | ⬜ planned                               |
| Basic operator GUI polish (CSS, search/filter)                      | ⬜ planned                               |
| Dockerfile for easy deployment                                      | ⬜ planned                               |

---

## Completion ideas (stretch)

* [ ] Rate‑limiting /auth throttling.
* [ ] Auto‑expire old logs & compress.
* [ ] Obfuscated traffic patterns (padding, random jitter).
* [ ] Domain‑fronted endpoints.

---

### Quick start

```bash
# dev server
make run   # requires Python 3.13+

# tests
make test  # runs pytest with pre‑commit config
```

