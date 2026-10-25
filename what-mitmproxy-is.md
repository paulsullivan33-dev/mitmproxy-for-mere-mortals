# What mitmproxy Is

When a program on your machine fetches
something from the web — a page, an API
answer, an update — it opens a connection
to a server and holds a conversation in
**HTTP**: a request goes out (*GET this,
here are my headers, here is my data*), a
response comes back (*200 OK, here are my
headers, here is the page*). Your browser
shows you the rendered result. The
conversation itself scrolls past unseen.

**mitmproxy is a program you place in the
middle of that conversation.** It is a
**proxy**: your client is told to send its
requests to mitmproxy instead of directly
to the server. mitmproxy receives each
request, shows it to you, passes it on to
the real server, receives the response,
shows you that too, and hands it back to
the client. Each request-and-response pair
it handles is called a **flow**, and flows
are the thing you will spend the whole
guide reading, filtering, saving and
occasionally changing.

The name is the mechanism, honestly
labelled: *man in the middle*. Chapter 8
shows how the same trick works for
encrypted **HTTPS** traffic — two separate
encrypted connections, one to each side,
with mitmproxy reading in the middle.

## Why anyone would do this

Four honest reasons account for nearly
every legitimate use:

- **Debugging.** Your script talks to an
  API and gets a puzzling answer. Was the
  request you *think* you sent the request
  you *actually* sent? A proxy settles it:
  here are the exact headers, the exact
  body, the exact response. No guessing,
  no logging code added in a hurry.
- **Learning.** Protocols are easier to
  understand from real traffic than from
  diagrams. Watching your own browser fetch
  a page — dozens of requests, redirects,
  cookies, caching — teaches more in ten
  minutes than a chapter of this guide can.
  (Chapter 13 of *this* guide is honest
  about what watching can and cannot show.)
- **Testing.** If your program must cope
  with a slow server, an error, a mangled
  response, a proxy can manufacture those
  conditions on demand — chapter 9's addons
  change traffic in flight, and chapter 11
  has the recipes.
- **Checking up.** A program on your own
  machine sends *something* home. To whom,
  how often, containing what? Your traffic,
  your machine: a fair question, and a
  proxy answers it.

## The rule, stated before everything else

A tool that can read your traffic can
read *anyone's* traffic it is placed in
front of, and HTTPS interception (chapter
8) works only because a machine has been
told to *trust* the interceptor. So this
guide has one rule, and it is not fine
print:

> **Inspect only traffic that is yours —
> on machines you own, or where every
> party involved has given you explicit
> permission.**

Debugging your own app: yes. Watching
your own browser learn what your smart TV
sends home from your own network: that is
your network and your television, and
still worth a moment's thought about
anyone else who uses them. A partner's
phone, an employer's laptop, the café's
other customers, a "quick look" at what
an app sends from someone else's account:
no — in many places that is a crime as
well as a betrayal, quite apart from what
this guide thinks of it. The lab in this
guide went further than most readers will
need to: every capture was between two
programs on one machine, talking to a
server written for the purpose, and the
one "secret" in the HTTPS chapter was
invented for the occasion and sent by the
lab to itself.

If a future idea you have for this tool
does not fit inside the rule, the idea is
the problem. Chapter 13 returns to this
with the legal edge spelled out a little
further.

## A familiar shape

mitmproxy is one program with three faces
(chapter 2): an interactive console for a
terminal, **mitmdump** — the scriptable
face, which prints flows as text and is
what most of this guide's lab used — and
**mitmweb**, which serves a web page you
drive from a browser. All three run the
same engine on the same flows, so learning
one teaches the others.

A first taste, after installing
(chapter 3):

```bash
mitmdump -p 8080 -w my-first.mitm
curl --noproxy '' -x http://127.0.0.1:8080 http://127.0.0.1:18080/hello
```

The first command starts the proxy on
port 8080, saving every flow to a file.
The second asks a practice server —
running on the same machine, chapter 4
builds one — for its `/hello` page, *via*
the proxy. mitmdump prints the flow as it
passes, and the file keeps it for
chapter 5.

Check: mitmdump's output shows the request
line and the answering status, as in the
lab's transcript `mitmproxy-lab/transcripts/t01-http-capture.txt`:

```text
127.0.0.1:59850: GET http://127.0.0.1:18080/hello
              << 200 OK 164b
```

## Who it is for

The developer whose API call came back
wrong and who wants evidence instead of a
theory. The curious owner of a house full
of chatty devices, asking what the chatter
contains. The student of networks who
learns by watching. The common thread is
one person, their own machines, and a
question that only the traffic itself can
answer.

## What it is not

mitmproxy is not a packet sniffer: it
sees the conversations it proxies, whole
and decoded — not every packet on the
wire (that is Wireshark's country,
chapter 12). It is not a scanner or an
attack tool: it does not find other
machines' weaknesses, and pointing it at
services you do not run crosses the rule
above. It is not a VPN and not an
anonymiser: it stands in the open between
a client that chose it and a server, and
both can tell. And it is not invisible:
a client that checks certificates
seriously will refuse its HTTPS
interception outright (chapter 13), which
is the correct behaviour, and this guide
treats it as a limit, not a puzzle.
