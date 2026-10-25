# The Neighbours

mitmproxy is not the only seat from which
traffic can be watched, and several of its
neighbours see things it cannot. An honest
map:

## The browser's developer tools

Every desktop browser carries a Network
panel: the requests that page made, with
headers, timing and previews, one click
from the page itself. For pure *web page*
debugging this is often the right tool —
no proxy to configure, no CA to trust,
and it sees the browser's own view
(cache hits, service workers) that a proxy
never can. Its limits are its walls: one
browser, one profile, no other programs,
and nothing saved in a form you can
script against afterwards. mitmproxy is
the answer when the client is not a
browser, or when the recording must
outlive the session.

## Wireshark and tcpdump

The packet tools (this series has a
Wireshark guide) watch the wire itself:
every packet, every protocol, whether or
not the traffic was addressed to them.
They see what mitmproxy structurally
cannot — DNS lookups, the TLS handshake
in its armour, protocols that are not
HTTP at all, traffic from programs that
ignore proxy settings entirely. What they
cannot easily give you is the
*conversation*: HTTPS in Wireshark is
ciphertext unless you feed it session
keys, and a request's body is an exercise
in reassembly. The tools are complements,
not rivals: packets to prove where bytes
went, a proxy to read what the bytes
*said*.

## Charles Proxy

The long-standing commercial neighbour on
macOS and Windows: a polished GUI proxy
with throttling, breakpoints and
repeat-request tools that clearly taught
the species its manners. If a team already
licenses it and lives in its UI, it does
the chapter-1-to-9 jobs well. mitmproxy's
counter-offer is being open source,
scriptable in Python end to end, and at
home in a terminal and a CI job.

## Fiddler

The Windows classic, now cross-platform
as Fiddler Everywhere: HTTPS interception
with an approachable interface and a
session list generations of developers
learned on. Its auto-responder is server
replay (chapter 10) with good tailoring.
The trade against mitmproxy is the same
shape as Charles': a product with a
licence and a UI, versus a tool with a
scripting engine and a command line.

## Burp Suite

The security professional's proxy: an
interception core surrounded by a scanner,
an intruder (automated attack) tool, and
two decades of web-testing craft. If your
job is assessing *other systems'* security
— with a contract that says so — Burp is
the trade's standard and this guide is no
substitute. For watching your *own*
traffic and learning, it is a siege engine
brought to open a letter. Chapter 1's rule
is the difference between the two books
that could be written about either tool.

## A plain HTTP echo and logging

Sometimes the neighbour is smaller: an
echo service (the lab's is
`mitmproxy-lab/server/`), a server's own
access log, a `curl -v`. Half of debugging
is asking the traffic a yes/no question,
and those need a yes/no tool. Reach for
the proxy when the question is *show me
the conversation*; reach for the small
tools when it is *did it arrive at all*.
