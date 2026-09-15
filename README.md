# Pyro5 Protocol — Service Discovery

## Carlos Viramontes

## 901099619

## Overview

In this assignment, you will **implement service discovery** by querying a **name server** to discover what services are available in the registry.

By the end, you'll have written a from-scratch Pyro5 client (in Java or Python) that:
1. Connects to the name server on `localhost:9090`
2. Sends a request to list all registered services
3. Parses the response (serpent serialization)
4. Extracts and prints all service names and their URIs

This teaches you how distributed systems handle **dynamic service discovery** — the same pattern used by Kubernetes, Consul, and enterprise service meshes.

---

## Background: Name Servers in RPC

In a distributed system, services are often **not at fixed addresses**. Instead:

1. **Service registration:** When a server starts, it registers itself with a name server (e.g., "test.echoserver is at 127.0.0.1:57449")
2. **Service discovery:** When a client needs to call that service, it queries the name server (e.g., "where is test.echoserver?")
3. **Dynamic updates:** If a server restarts, it gets a new port and re-registers; clients automatically find it next time

This makes systems **resilient** (servers can move, restart, scale) and **decoupled** (clients don't hardcode server addresses).

Pyro5's name server is exactly this: a registry that answers "where is service X?"

### Language Independence

This assignment demonstrates a crucial principle: **RPC/RMI protocols are language-independent**. The Pyro5 name server is written in Python, but your client can be in **Java or Python**. Both will:
- Send the same wire protocol bytes
- Receive the same response format
- Produce identical output

What matters is the **protocol itself**, not the language. This is why microservices can talk to each other regardless of implementation — they speak a common language: the wire protocol.

---

## Setup: Install Dependencies

Before starting, install Pyro5:

```bash
pip install Pyro5
```

Verify the installation:
```bash
python -m Pyro5.nameserver --help
python -m Pyro5.nsc --help
```

---

## Part 1: Observe (20 min)

### 1.1 Start the Infrastructure

**Terminal 1 — Name Server:**
```bash
python -m Pyro5.nameserver
# or: pyro5-ns
```

Output:
```
Not starting broadcast server for IPv6.
NS running on localhost:9090 (::1)
URI = PYRO:Pyro.NameServer@localhost:9090
```

### 1.2 Query the Name Server (using nsc CLI)

**Terminal 2 — Query the name server:**
```bash
python -m Pyro5.nsc list
```

Example output:
```
--------START LIST 
Pyro.NameServer --> PYRO:Pyro.NameServer@localhost:9090
    metadata: {'class:Pyro5.nameserver.NameServer'}
--------END LIST
```

**Key insight:** The name server returns a list of all registered services with their URIs and metadata. This output format is what your client must replicate exactly.

### 1.3 Capture Network Traffic with Wireshark

Observe the actual network protocol when you query the name server:

```bash
# start wireshark and listen to lo0 (loopback)

# Terminal 1 (already running): Pyro5 name server

# Terminal 2: Query the name server
python -m Pyro5.nsc list
```

In Wireshark, you'll see:
1. **List request** (client → name server): "what services are registered?"
2. **List response** (name server → client): Dictionary of service names and URIs

Both use **serpent serialization** (Pyro5's native binary format).

### 1.4 Study the Captured Traffic

Annotate the captured traffic frame by frame and create an ANNOTATED.md file. Look for:
- **Pyro5 magic header** (`PYRO` in 4 ASCII bytes at offset 0-3)
- **Message type** (which number?)
- **Serializer ID** (should be 4 for serpent)
- **Payload** (the actual service list request and response in serpent format)

---

## Part 2: Implement — Service Discovery Client

### 2.1 Design

Your client must:

1. **Open a TCP socket** to the name server at `localhost:9090`
2. **Send a Pyro5 message** requesting to list all registered services (prefix = "")
3. **Receive the response** (a Pyro5 message containing a dictionary of service names, URIs, and metadata)
4. **Parse the response** using serpent deserialization
5. **Extract all service names, URIs, and metadata** from the parsed response
6. **Print each service** in the same format as `pyro5-nsc list`
7. **Close the connection** gracefully

**Output format (must match `pyro5-nsc list` exactly):**
```
--------START LIST 
Pyro.NameServer --> PYRO:Pyro.NameServer@localhost:9090
    metadata: {'class:Pyro5.nameserver.NameServer'}
--------END LIST
```

### 2.2 Implement

Write your client in your language of choice.

**File structure:**
- `src/ServiceDiscoveryClient.java` (or `service_discovery_client.py` if Python)
- `src/PyroMessage.java` (or `pyro_message.py`): Helper class for Pyro5 wire protocol

**Key functions to implement:**

These are recommendations, you have the flexibility to create whatever
methods you see fit.

1. **`build_list_request(prefix)`** — Create a Pyro5 method-call message
   - Serialize the request as serpent: `("Pyro.NameServer", "list_prefix", ("",), {})`
   - Wrap in Pyro5 header (20 bytes: magic + version + flags + serializer + size)
   - Return the complete message bytes

2. **`send_message(socket, message)`** — Send bytes over socket
   - Call `socket.send(message)`

3. **`receive_message(socket)`** — Receive and parse a Pyro5 response
   - Read 20-byte header
   - Extract message size
   - Read that many bytes
   - Return the response payload

4. **`parse_services(response)`** — Extract the service dictionary from serpent response
   - Deserialize serpent manually (both Java and Python should parse the binary format)
   - Extract the returned dictionary (names → URIs)
   - Extract metadata if present
   - Format and print output matching `pyro5-nsc list` format

### 2.3 Test Locally

Before submitting:

```bash
# Terminal 1: Name server
python -m Pyro5.nameserver

# Terminal 2: Your client
# Java:
javac src/*.java
java -cp src ServiceDiscoveryClient

# Python:
python service_discovery_client.py
```

Expected output (must match `pyro5-nsc list` exactly):
```
--------START LIST 
Pyro.NameServer --> PYRO:Pyro.NameServer@localhost:9090
    metadata: {'class:Pyro5.nameserver.NameServer'}
--------END LIST
```

**Tip:** You can verify your output matches by comparing with:
```bash
python -m Pyro5.nsc list
```

---

## Part 3: Grading Rubric

Your submission will be graded on:

- **Traffic analysis:** Did you annotate the captured traffic, explaining the Pyro5 message structure (header, serializer, payload) for a service list request?
- **Client implementation:**
  - Does your client correctly build a Pyro5 service listing request?
  - Does it send it to the name server on `localhost:9090`?
  - Does it receive and parse the response (serpent serialization)?
  - Does it correctly extract all service names and URIs?
  - Does it print all services in a readable format?
  - Is the code readable and well-commented?
  - Does it handle errors gracefully?
- **CI/CD:** Does your code pass all the CI/CD tests including having unit
  tests for your methods?
- **Grading hook:** Your client, run unmodified via `java -cp src ServiceDiscoveryClient` (Java) or `python service_discovery_client.py` (Python), produces **identical output** to `python -m Pyro5.nsc list` when the real Pyro5 name server is running.

---

## Resources

Cite any resources you used. Include:
- Pyro5 wire protocol: https://pyro5.readthedocs.io/en/latest/api/protocol.html
- SERPENT\_FORMAT.md
- PYRO5\_CLI.md
- Any other sources

---

## Academic Integrity & Professional Practices

**You are encouraged to use all available resources.** This mirrors real professional development:

✅ **DO:**
- Search Stack Overflow, documentation, GitHub
- Use AI (Claude, ChatGPT, Copilot) for explanations, debugging, ideas
- Copy code from tutorials, examples, open-source projects
- Ask classmates, TAs, instructor for help
- Use libraries, frameworks, and tools

❌ **DON'T:**
- Copy code without understanding it (don't just paste and submit)
- Submit work that's entirely generated by AI without your input
- Claim you wrote code you didn't write

**The requirement:** **Cite all sources in a `SOURCES.md` file.** Include:
- AI tools used (e.g., "Used Claude to explain serpent parsing")
- Stack Overflow links
- Documentation pages
- GitHub repos
- Classmates who helped

**Penalty for missing citations:** Automatic zero on assignment, regardless of code quality. Missing even one source = failure.

**Why?** Professionals cite sources, give credit, and know what they use. Learn to work like a real engineer: use all tools, but be transparent.

---

**Submission:** Push your code to your Classroom50 repo for this assignment.

Claude (Anthropic) was used to help design this assignment and create the documentation.
