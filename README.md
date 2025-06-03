# CYBR473 Assignment 3 – Proof‑of‑Concept Malware & C2

Welcome! This repository is split into two main components:

* **CommandAndControl** – Flask‑based C2 server ([README](CommandAndControl/README.md))
* **Malware** – Windows client keylogger ([README](Malware/README.md))

---

## Global checklist

| Task                                                         | Status  |
| ------------------------------------------------------------ | ------- |
| Set up Git repo with Makefile + pre‑commit test gate         | ✅ done  |
| Integrate assignment brief into planning docs                | ✅       |
| Draft phishing email (.txt) convincing victim to run malware | ⬜ to‑do |
| Record narrated demo video (≤ 5 min)                         | ⬜ to‑do |
| Package malware as 32‑bit Windows executable                 | ⬜ to‑do |
| Prepare submission archive (source, binary, video, README)   | ⬜       |

---

### Quick start for assessors

```bash
# C2 server
cd CommandAndControl
make run

# (Later) Build & execute malware client on test VM
```

All coursework requirements are referenced directly from **assignment\_brief.txt** in repo root.

