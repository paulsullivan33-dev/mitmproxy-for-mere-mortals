# Reading Flows

A capture you cannot read back is just a
rumour. This chapter opens the flow file
from chapter 4, lists what is inside, and
takes one flow apart until there is
nothing left in it you cannot name.

## Reading a flow file

You do not need the proxy running to read
a recording. `-r` reads instead of
listening, and `-n` says no server at all:

```bash
mitmdump -nr lab-http.mitm
```

(transcript t02):

```text
127.0.0.1:59850: GET http://127.0.0.1:18080/hello
              << 200 OK 164b
127.0.0.1:59866: GET http://127.0.0.1:18080/search?q=teapot&page=2
              << 200 OK 181b
127.0.0.1:59878: POST http://127.0.0.1:18080/plants
              << 200 OK 257b
127.0.0.1:59888: GET http://127.0.0.1:18080/missing
              << 404 Not Found 166b
```

One flow takes two lines in this summary
view: the request, then `<<` and the
response's status and body size. The
number before the colon on the left is the
client's own port for that connection — how
you tell two otherwise identical requests
apart.

## One flow, in full

Raise the detail with the `flow_detail`
option — 1 is the summary above, 4 is
everything mitmdump knows how to print:

```bash
mitmdump --set flow_detail=4 -nr lab-http.mitm "~u /plants"
```

(the `~u /plants` part is a filter —
chapter 6 — picking the one flow whose
URL matches). The lab's output, trimmed of
nothing that matters (transcript t02):

```text
127.0.0.1:59878: POST http://127.0.0.1:18080/plants
    Host: 127.0.0.1:18080
    User-Agent: curl/8.5.0
    Accept: */*
    Proxy-Connection: Keep-Alive
    Content-Length: 20
    Content-Type: application/x-www-form-urlencoded

    name: fern
    soil: moist

 << 200 OK 257b
    Server: BaseHTTP/0.6 Python/3.12.3
    Date: Sun, 25 Oct 2026 02:23:14 GMT
    Content-Type: text/plain; charset=utf-8
    Content-Length: 257

    served-by: plain-echo-server
    method: POST
    path: /plants
    ...
    body:
    name=fern&soil=moist
```

Walk it once, top to bottom:

- **Request line.** Method, full URL,
  and later (in the console and web views)
  the timing: when the request arrived,
  how long the server took.
- **Request headers.** Indented under the
  request: who the client claims to be
  (`User-Agent`), what it accepts, and the
  giveaway from chapter 4,
  `Proxy-Connection`, present because curl
  knew it was talking to a proxy.
- **Request body.** The form data,
  **decoded by mitmdump**: `name: fern`,
  `soil: moist`. On the wire this was
  `name=fern&soil=moist`, as the echo
  server's own report at the bottom shows.
  Decoding is a courtesy the tool extends
  to form posts, JSON, and several other
  common shapes — and a thing to remember:
  you are reading an interpretation, and
  for an argument about exact bytes, the
  raw body is one view away in the console
  and web faces.
- **Response line.** `<<`, the status code
  and its name, and the body size.
- **Response headers and body.** The
  server's side of the story — here, the
  echo server's report, which is why this
  flow contains the request *twice*: once
  as mitmproxy recorded it, and once as
  the server described receiving it. When
  the two disagree someday — a header
  present in one, missing in the other —
  you will have found something real:
  something between the seats changed the
  traffic. Chapter 9 will make that
  something be *you*.

## What else a flow holds

The printed views are summaries of a
richer object. A flow also records the
client and server addresses, the TLS
details of both connections when there are
any (chapter 8), redirects already
followed, WebSocket messages when the
conversation upgrades, and any error —
a flow can end in failure, and the file
keeps failures too, marked as errors
rather than responses. The console and
mitmweb (chapter 7) show all of it in
panels; mitmdump's `flow_detail` shows
most. An addon (chapter 9) sees *all* of
it, as Python objects, while it is live.

## Keeping recordings

A flow file keeps everything, including
things people typed into forms — in the
lab, a fern's soil preference; in real
browsing, passwords, session cookies,
personal messages. Treat flow files the
way chapter 3 treats the CA folder: they
are evidence about you, possibly about
anyone whose traffic you were permitted
to record, and they deserve the same
handling as the data they contain. Save
them where you would save the secrets in
them, delete them when the question is
answered, and never attach one to a
public bug report without reading every
flow in it first. Chapter 6's filters
double as the redaction tool: read a file
in, keep only the flows that match, write
those out, and share the smaller file.
