# Addons — Writing Your Own

Watching traffic answers questions.
Changing it answers *better* questions:
does the app cope when the server is slow,
when a header is missing, when the answer
has a field it has never seen? An **addon**
is how you make those changes — a small
Python script whose functions mitmproxy
calls as each flow passes. This chapter
writes the lab's addon, runs it, and reads
the echo server's verdict.

## The shape of an addon

An addon is a Python file defining any of
a set of named **hooks**. The two that
matter most:

```python
from mitmproxy import http

def request(flow: http.HTTPFlow) -> None:
    # called when a request arrives,
    # before it is sent to the server

def response(flow: http.HTTPFlow) -> None:
    # called when the response arrives,
    # before it is returned to the client
```

Inside a hook, `flow.request` and
`flow.response` are live objects: their
headers are dictionaries you can set,
their bodies are bytes (or text, via
`.text`) you can rewrite, and changing
them changes what actually travels.
Load an addon with `-s`:

```bash
mitmdump -p 8080 -s labnotes.py
```

## The lab's addon

The lab's addon (kept at
`mitmproxy-lab/addons/labnotes.py`, and
small enough to print whole) does two
visible things:

```python
from mitmproxy import http


def request(flow: http.HTTPFlow) -> None:
    flow.request.headers["X-Lab-Note"] = "added-by-the-lab-addon"


def response(flow: http.HTTPFlow) -> None:
    flow.response.headers["X-Lab-Note"] = "answered-through-the-lab-addon"
    content_type = flow.response.headers.get("Content-Type", "")
    if content_type.startswith("text/plain"):
        flow.response.text = (
            flow.response.text + "[annotated by the lab addon]\n"
        )
```

On the way out, every request is stamped
with a header, `X-Lab-Note`. On the way
back, every response gets a matching
header, and plain-text bodies gain a
footer line. Setting `.text` (rather than
raw bytes) lets mitmproxy handle lengths
and encoding — it repairs the
`Content-Length` for you, which the
transcript shows happening.

## The evidence

Same request as chapter 4, twice
(transcript t03). Without the addon, the
echo server reports the headers it
received: Host, User-Agent, Accept,
Proxy-Connection — and nothing else. With
`mitmdump -s labnotes.py`:

```text
HTTP/1.1 200 OK
...
X-Lab-Note: answered-through-the-lab-addon

served-by: plain-echo-server
method: GET
path: /hello
headers:
  Host: 127.0.0.1:18080
  User-Agent: curl/8.5.0
  Accept: */*
  Proxy-Connection: Keep-Alive
  X-Lab-Note: added-by-the-lab-addon
body:

[annotated by the lab addon]
```

Three witnesses agree. The server's own
report lists `X-Lab-Note:
added-by-the-lab-addon` among the headers
it *received* — the stamp is not a display
trick; it crossed the network. The
response headers shown by curl carry the
response stamp. And the body ends with the
annotation line, the response length
grown from 164 to 230 bytes to prove the
rewrite went out on the wire, not just
into a log. mitmdump's flow line records
the new size (`<< 200 OK 230b`), a third
confirmation.

That is the pattern for testing any addon:
**a server that reports what it received,
and a before/after pair.** An addon that
"should" change traffic and a feeling that
it does are worth nothing next to an echo.

## What else hooks can do

The full hook list is in the project's
"Addons" documentation; the useful shelf:

- `request` / `response` — read, stamp,
  rewrite, as above.
- Answering *instead of* the server: set
  `flow.response` inside `request` and the
  request never travels — a mock server in
  five lines, for testing a client against
  answers you script.
- Killing a flow: `flow.kill()` drops it,
  the client sees a failure — the "what if
  this call dies?" test.
- Logging with judgement: an addon that
  prints or saves only flows matching its
  own conditions is a filter (chapter 6)
  with a memory.
- Delaying: hooks are ordinary Python; a
  sleep in `response` is a slow server, on
  exactly the routes you choose.

Two restraints. An addon runs on **every**
flow, so a slow or crashing hook degrades
or breaks all traffic through that proxy —
test against the echo server, where a
mistake costs nothing. And an addon that
rewrites *other people's* traffic is
chapter 1's line crossed with tooling:
the same file that stamps your practice
requests would stamp a housemate's, which
is why addons, like captures, stay inside
the rule.
