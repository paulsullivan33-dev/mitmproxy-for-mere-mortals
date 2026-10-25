# Glossary

**Addon** — a Python script loaded with
`-s`, whose hook functions mitmproxy calls
as flows pass; it may read, change or drop
traffic (chapter 9).

**Certificate authority (CA)** — a key and
certificate able to sign other
certificates. mitmproxy creates its own in
`~/.mitmproxy` on first run (chapter 3).

**Certificate pinning** — an app accepting
only a specific certificate or authority
for a server, refusing all others —
including a trusted CA's minted ones
(chapter 13).

**Client replay** — sending recorded
requests from a flow file again
(`mitmdump -C`, chapter 10).

**CONNECT** — the HTTP method a client uses
to ask a proxy for a tunnel to an HTTPS
server; the door through which chapter 8
walks.

**Filter** — an expression in mitmproxy's
filter language (`~m POST`, `~c 404`, …)
selecting which flows an operation touches
(chapter 6).

**Flow** — one request and its response,
with headers, bodies, timing and
connection details; the unit everything in
mitmproxy reads, saves and changes
(chapter 5).

**Flow file** — a file of recorded flows,
written with `-w`, read with `-r`, in
mitmproxy's own format.

**Hook** — a named function in an addon
(`request`, `response`, …) that the core
calls at a fixed point in a flow's life.

**HTTPS interception** — reading HTTPS by
holding two encrypted connections, one to
each side, made possible by the client
trusting the proxy's CA (chapter 8).

**Man in the middle** — a party seated
between two others' conversation, able to
read (and, in principle, alter) what
passes. mitmproxy's name and honest
description.

**mitm.it** — the address a proxied
browser visits to download the CA
certificate for its platform (chapter 8).

**mitmdump** — the scriptable face of
mitmproxy: flows as printed text, made for
saving, filtering and addons.

**mitmweb** — the web face: the proxy plus
an interface in a browser, on its own
token-protected port (chapter 7).

**Mode** — the shape by which traffic
reaches the proxy: regular (the client is
told), reverse, transparent, WireGuard,
local (chapter 2).

**no_proxy** — an environment variable
listing addresses clients must reach
*directly*, honoured even over an explicit
proxy setting; the empty capture's best
friend (chapters 4 and 14).

**Proxy** — a program that fetches on a
client's behalf, standing between client
and server by arrangement.

**Regular mode** — the mode where the
client is configured to use the proxy —
the only mode this guide's lab ran.

**Self-signed certificate** — a
certificate signed by its own maker rather
than a known authority; the lab's server
wore one, and chapter 8's proxy rightly
refused it at first.

**Server replay** — answering incoming
requests from a flow file's recordings
(`mitmdump -S`): a mock built from a
capture (chapter 10).

**SSL/TLS** — the encryption under HTTPS.
The protocols are all TLS now; SSL
survives in option names like
`--ssl-insecure`.

**Trust store** — the collection of CAs a
client (or a whole operating system)
accepts as signers; installing
mitmproxy's CA adds it to one (chapter 8).

**Upstream** — from the proxy's seat, the
real server's direction; the client's
direction is downstream. A 502 about
certificate verification names the
upstream side (chapter 14).
