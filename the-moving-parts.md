# The Moving Parts

mitmproxy has more pieces than its one
command suggests. Knowing which piece
holds what is the difference between "the
proxy is broken" and "curl never sent the
request here" — a real distinction, as
this guide's own lab learned (chapter 14).

## The proxy core

The engine is a server that listens on a
port you choose — **8080** by default — and
speaks the proxy dialect of HTTP. A client
connects to it and asks it to fetch a URL.
The core opens its own connection to the
real server, relays the conversation both
ways, and assembles each exchange into a
**flow**: one object holding the request,
the response, the timing, and the
connection details. Everything else in
this chapter is a way of looking at flows
or changing them.

For plain HTTP, relaying is enough. For
HTTPS the client asks the proxy to open a
**CONNECT** tunnel; what the core does
with that tunnel is chapter 8's whole
story.

## The three faces

One engine, three interfaces. They share
options, flow files and addons, so nothing
you learn in one is wasted in another.

| Face | Command | Shape |
|---|---|---|
| Console | `mitmproxy` | An interactive terminal window: flows in a list, keys to open, edit, replay |
| Script | `mitmdump` | No window: flows printed as text lines, made for saving, filtering and scripts |
| Web | `mitmweb` | A page in your browser: the console's list-and-detail view, served on its own port |

The console is where most people explore.
mitmdump is where work gets *recorded* —
this guide's lab drove almost everything
through mitmdump because its output can be
kept in a transcript and checked, and
because anything you can do there can be
put in a script. mitmweb (chapter 7) is
the friendliest face and the one the lab
verified live alongside mitmdump; the
console is described from the
documentation, and `criteria.md` says so.

## The certificate authority

On its first run, mitmproxy creates a
folder, **`~/.mitmproxy`**, and inside it
a small **certificate authority (CA)** —
a private key and a certificate that can
sign other certificates. This is the piece
that makes HTTPS interception possible:
when a client connects through the proxy
to `https://example.com`, mitmproxy mints
a certificate *for that name*, signed by
its CA, on the spot. A client that trusts
the CA accepts the minted certificate, and
the encrypted conversation happens with
mitmproxy instead of the server — while
mitmproxy holds a second encrypted
conversation with the real server. Two
locks, two keys, one reader in the middle.
Chapter 8 walks the whole exchange, and
chapter 3 shows the files. Treat the
folder with respect: whoever holds that
private key can impersonate any site to
any machine that trusts the CA (chapter
13).

## Addons

An **addon** is a small Python script,
loaded with `-s`, whose functions the core
calls as traffic passes: `request(flow)`
before a request goes out, `response(flow)`
after the answer comes back, and others
for errors, connections and startup. The
addon receives the live flow object and
may read it, stamp it, rewrite it or drop
it. Chapter 9 writes one for real — about
a dozen lines that put a visible mark on
every conversation — and it is the feature
that turns mitmproxy from a viewer into an
instrument.

## Flow files

Flows can be written to a file with `-w`
and read back with `-r` — in any of the
three faces, days later, on another
machine. A flow file is the unit of
evidence in this guide: the lab's captures
live in one, chapter 5 reads one back and
takes it apart, chapter 6 filters it, and
chapter 10 replays requests from one.
The format is mitmproxy's own; a flow file
from an old version is upgraded as it is
read.

## Modes: how traffic reaches the proxy

"Being a proxy" has several shapes. This
guide teaches the first and names the
rest; only the first was run in the lab.

| Mode | How traffic arrives | Lab status |
|---|---|---|
| **Regular** | The client is *told* to use the proxy: a setting, an option, an environment variable | **Run** (all transcripts) |
| Reverse | The proxy stands in front of one server and clients connect to it as if it were the server | Documented only |
| Transparent | The network redirects traffic to the proxy whether the client knows or not; needs routing privileges | Documented only |
| WireGuard | Devices connect to a WireGuard tunnel the proxy provides, and their traffic arrives through it | Documented only |
| Local / per-application | mitmproxy intercepts named programs on the same machine, by operating-system hooks | Documented only |

Regular mode is the honest beginner's
mode — the client opted in, which matches
this guide's rule — and it is enough for
browsers you configure, programs with a
proxy setting, and every command-line tool
that honours `-x` or an environment
variable. The other modes exist for
clients that cannot be told: an app with
no proxy setting, a device you own but
cannot configure. They demand privileges
(root on a router, a tunnel the device
joins) precisely because they override a
client's choices, which is one more reason
this guide insists on the permission rule
from chapter 1.

## Who holds what, when it breaks

- The **client** decides whether the proxy
  is used at all — and can quietly decide
  *not* to, for some addresses (chapter
  14's `no_proxy` trap lives here).
- The **core** holds the flows, in memory,
  and the flow file holds them afterwards.
- The **CA** holds the trust. Lose control
  of `~/.mitmproxy` and you lose the
  meaning of every padlock on that machine.
- An **addon** holds the power to change
  things; a buggy addon changes *every*
  thing, which is why chapter 9 tests
  against a practice server first.
