# mitmproxy for Mere Mortals

A web browser talks to a server in
requests and responses: *give me this
page*, *here it is*. Normally those
conversations happen out of sight, and all
you see is the finished page. **mitmproxy**
sits between the two sides and lets you
watch — every request with its headers and
body, every response the same — and, when
you ask it to, change what passes through.
It is a **proxy** you run yourself, on
your own machine, mostly to answer one
question: *what did my program actually
send, and what actually came back?*

This guide explains how that works, how
to take your first capture against a
practice server on your own machine, how
to read what a **flow** contains, filter a
hundred flows down to the three that
matter, look inside HTTPS with a
certificate authority you control, and
write small Python **addons** that stamp,
annotate or rewrite traffic. The limits
are stated plainly, including the big one:
the same machinery that debugs your own
app can read other people's secrets, and
this guide is only about the first of
those.

The rule that governs everything here is
stated in chapter 1 and repeated in
chapter 13: **your traffic, your machines,
or traffic you have explicit permission
to inspect.** The lab obeyed it strictly.
Every capture in this guide is between
programs the lab itself ran, on one
machine, over addresses that never leave
that machine.

The lab behind this guide ran the real
thing: **mitmproxy 12.3.0**, installed
with pip into a fresh virtual environment
on a small Linux machine, against a
throwaway **echo server** the lab wrote
for the purpose — a tiny program that
answers every request with a report of
what it received, so changes made in the
middle are visible in the reply. Against
it the lab captured plain HTTP flows and
saved them to a file, read the file back
and filtered it four ways, ran an addon
that stamped a header onto requests and
annotated responses (proven by the echo
server's own report), served the echo
server over HTTPS with a certificate the
lab made itself, watched mitmproxy refuse
that certificate until it was told not to
verify it, taught curl to trust
mitmproxy's own certificate authority,
and read the decrypted recording — a
secret the lab made up, sitting in clear
text in the flow file. The web interface
was started and driven through its
token-protected front door, and recorded
requests were replayed at the server a
second time.

What the lab could not do, it did not
fake. It had one machine and no spare
devices, so pointing a phone or a second
computer at the proxy, installing the
certificate authority into a real
operating system's trust store, and the
proxy modes that need network privileges
(transparent mode, WireGuard mode,
per-application interception) are taught
from the documentation and labelled as
such wherever they appear. The console
interface, mitmproxy proper, is likewise
described rather than demonstrated: the
lab drove the same engine through its
scriptable face, mitmdump, and its web
face, mitmweb, and says so.
`criteria.md` keeps the full ledger of
what was run and what was only read.

## What this guide covers

- [**What mitmproxy is**](what-mitmproxy-is.md) —
  the mental model: a seat between the
  client and the server, what a flow is,
  and the ethics that are part of the
  tool, not an afterthought
- [**The moving parts**](the-moving-parts.md) —
  the proxy core, the three faces
  (console, mitmdump, mitmweb), the
  certificate authority, addons, and the
  modes, and which part holds what
- [**Installing mitmproxy**](installing-mitmproxy.md) —
  the pip install and the standalone
  installers, the first run, and the
  `~/.mitmproxy` folder where the
  certificate authority is born
- [**Your first capture**](your-first-capture.md) —
  a practice server on your own machine,
  pointing curl at the proxy, and the
  `no_proxy` trap that can make a working
  proxy look empty
- [**Reading flows**](reading-flows.md) —
  one flow taken apart: request line,
  headers, body, response, timing, and
  the flow file that keeps them
- [**Filters**](filters.md) —
  the filter language: matching by
  method, URL, status code and content,
  and combining tests until a haystack
  becomes a handful
- [**The console and the web UI**](console-and-web-ui.md) —
  mitmproxy's terminal console for
  interactive work, and mitmweb in a
  browser, behind its token
- [**HTTPS and the certificate authority**](https-and-the-ca.md) —
  how the man in the middle works:
  two encrypted connections pretending
  to be one, the CA that makes it
  possible, and both ways it can refuse
- [**Addons — writing your own**](addons.md) —
  small Python hooks that see every
  flow: stamping a request header and
  annotating a response, proven against
  the echo server
- [**Replay and resending**](replay-and-resending.md) —
  sending recorded requests again, and
  what replay can and cannot prove
- [**Recipes**](recipes.md) — find what
  an app really sends, slow a connection
  down on purpose, keep a clean recording
  of an API session, strip a header that
  should not leave the house
- [**The neighbours**](the-neighbours.md) —
  the browser's own developer tools,
  Wireshark and tcpdump, Charles,
  Fiddler and Burp Suite: what each sees
  that mitmproxy doesn't, and vice versa
- [**Limits**](limits.md) — pinned
  certificates refuse, not everything is
  HTTP, a trusted CA is a loaded key, and
  the legal and ethical edge, stated
  plainly
- [**Troubleshooting**](troubleshooting.md) —
  the empty capture, the certificate
  error with two different causes, the
  502 from a self-signed server, and the
  traps this guide's lab fell into so you
  don't have to
- [**Glossary**](glossary.md) — the
  terms, collected in one place

## What it doesn't cover

Intercepting traffic you do not own or
have permission to inspect — that is not
a harder chapter of this book, it is a
different and uglier activity, and
chapter 13 explains the line. Defeating
certificate pinning on other people's
apps, hiding a proxy from a network
administrator, and large-scale traffic
analysis are likewise out. Running
mitmproxy as shared infrastructure for a
whole organisation — accounts, audit
trails, policy — is pointed at, not
taught; this guide stays with one person
and their own machines, where the tool
does its honest work.

## How to use this guide

Read chapter 1 for the model and the
rules, and chapter 2 before installing
anything — knowing which part holds what
turns later confusion into a named
problem. Chapter 4 takes your first
capture in the same sitting as the
install, against a server on your own
machine; do not point the proxy at real
browsing until the practice runs feel
boring. Chapter 8 is not the optional
chapter: understand the certificate
authority before you trust it anywhere,
because a trusted CA is a key to every
encrypted conversation on that machine.
Chapter 9 is the one that turns a viewer
into a tool — write the addon while the
examples are small enough to check by
eye. The lab's transcripts live in
`mitmproxy-lab/transcripts/`; its echo
server is `mitmproxy-lab/server/` and its
addon `mitmproxy-lab/addons/`; its notes
are `examples/lab-notes.txt`.
