# The Console and the Web UI

mitmdump prints flows and moves on. The
other two faces — the console and mitmweb —
are for *lingering*: opening a flow,
reading it slowly, holding one back while
you decide what to do with it. They show
the same flows mitmdump prints; what they
add is your hands.

## The console: `mitmproxy`

Start it like the others:

```bash
mitmproxy -p 8080
```

and your terminal becomes a flow list:
one row per flow, newest at the bottom,
arrow keys (or `j`/`k`) to move, Enter to
open the highlighted flow into a detail
view with tabs for the request, the
response and the connection details, `q`
to come back, `Q` to quit. A filter typed
after pressing `f` narrows the list with
chapter 6's language. Two powers justify
the console's existence:

- **Interception.** Press `i` and give a
  filter, and matching flows *stop* —
  the request is held in the console,
  the client waits, and you may read it,
  edit it (headers, body, even the URL),
  then release it with `a` or kill it
  with `x`. This is the testing seat of
  chapter 1: what does the client do when
  the answer is slow, wrong, or never
  comes? You are the answer, manually.
- **Replay in place.** A selected flow
  can be resent with `r` — chapter 10's
  machinery, at a keystroke.

Honesty, per this guide's habit: the lab
drove the engine through mitmdump and
mitmweb, whose transcripts can be kept
and checked; a terminal console cannot be
transcribed the same way, so the console's
keys above are taught from the project's
documentation (`mitmproxy --help` and the
in-program help, `?` inside the console,
agree with them). Everything the console
*shows* is the flow data of chapter 5,
which the lab verified in full.

## The web UI: `mitmweb`

```bash
mitmweb -p 8080 --web-port 8081 --no-web-open-browser
```

mitmweb runs the same proxy (port 8080)
and serves its interface on a second port,
8081 by default. The startup message the
lab captured (transcript t05):

```text
HTTP(S) proxy listening at *:8080.
Web server listening at http://127.0.0.1:8081/?token=…
```

Two deliberate choices are visible there.
The web port binds to **127.0.0.1** — the
machine itself; the interface that can
read and alter your captures is not
offered to the network. And the address
carries a **one-time token**. Ask for the
page without it and mitmweb answers
**403**; the lab verified exactly that,
then followed the token address (which
sets a cookie) and got the interface:

```text
$ curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8081/
403
$ curl -s -c cookies.txt "http://127.0.0.1:8081/?token=<token from startup>"
200
$ curl -s -b cookies.txt http://127.0.0.1:8081/ | grep -o "<title>[^<]*</title>"
<title>mitmproxy</title>
```

In the browser, mitmweb is the console's
view with windows: the flow list down the
left, the selected flow's request and
response in panels, the chapter 6 filter
box at the top, and buttons for the same
intercept, edit and replay powers. It is
the friendliest face for showing a
capture to another human — a colleague
looking at "what the app sent" does not
need to learn the console's keys first.

The interface is also a small API. The
same address that serves the page serves
the flow list as JSON at `/flows` — the
lab asked, with its cookie, and received
the flow it had just proxied, as data
(transcript t05). Anything that can read
JSON can build on a capture: a report, a
diff between two sessions, a test that
fails when a flow looks wrong. That is
mitmweb's quiet superpower, and it is why
the token exists: a page that can hand
over every recorded secret should not be
an open door, even on a private network.

Check: with mitmweb running, send one
request through the proxy as in chapter 4
and refresh the page. The flow appears in
the list within a second — and `curl -s -b
cookies.txt http://127.0.0.1:8081/flows`
shows the same flow as JSON.

## Which face, when

- **Console** — interactive debugging,
  intercepting, editing by hand, working
  over SSH where a browser is awkward.
- **mitmweb** — exploring a capture with
  your eyes (and a second person's),
  and any time the JSON endpoint earns
  its keep.
- **mitmdump** — recordings you keep,
  addons, scripts, anything that must be
  reproducible — which is why this guide's
  evidence lives there.
