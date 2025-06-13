# CYBR473 Assignment 3 

Hello! This repository is split into two main components:


## Running and Compliation

### To start server: (i used Git CMD)

```bash
cd CommandAndControl
python -m venv venv
.\venv\Scripts\activate.bat
pip install flask
python server.py
```

### To compile malware:

```bash
cd Malware
./quick w (need mingw installed)
npx packed.exe malware.exe
```

## What i've done

- [x] Anti debugger: `anti_debug.h` (if present, exit)
	- For: "They may also run your malware executable in a debugger like OllyDbg or x64dbg for deep dynamic analysis. They may try to set breakpoints, trace execution, or step through code."
- [x] Anti VM: `anti_vm.h` (if inside one, exit)
	- For: "The defender may be analysing your malware for deep analysis inside a virtual machine, e.g. using VirtualBox"
- [x] Https: `network.cpp and server.py`
- [x] Persistence: `persistence.h`. This copies to `/System32` as `svchost32.exe` and adds registry key
	- For: "Reboot the client machines so that the malware will be forced to shut down."
	- And: "The defender may look for suspicious processes or unusual binaries on disk. They may trust processes signed by Microsoft or running from `**C:\Windows\System32**`."
- [x] Randomised traffic timing: `utils.h::get_random_sleep_interval`. Used in exfiltration_worker, beacon, registration timer
- [x] Keylog data stored in inmemory buffer
	- For: "The defender may look for evidence of keylog files on infected machines."
- [x] make window disappear after running
	- start of main
- [x] Have it delete its original file after running (already copies itself to system32)
- [x] Anti-disassembly (add instructions to binary): `utils.h`
	- For: "You know that they are likely to use a disassembler like IDA-pro or ghidra to analyse your malware"
- [x] pack with upx
