Command and control architecture [10%]

Your malware must register itself with a central HTTP server (the Command-and-Control, a.k.a C&C, a.k.a. C2) to receive commands and transfer exfiltrated data. For testing purposes and for convenience, you may choose to run the C2 on localhost.

Your malware should generate a unique ID for itself based upon host information as described in the book. It should be uniquely identifying to allow the malware to receive instructions in the future.

Your C2 server should expose an HTTP interface that allows basic interaction, such as:

* GET /clients → List of registered malware clients with their IDs, and their status (active/inactive), and a link to display the collected keylogs of that client

* GET /logs/{id} → Displays exfiltrated keystrokes for a given client

Command execution [5%]

You must implement the following commands:

    slp id n: puts the malware id to sleep for n seconds.
    shd id: causes the malware id to shut itself down.
    pwn id: display a fun message at the client, like "sorry, you've been pwned, for educational purposes!", or something else, that alarms the victim that their system is infected! 

