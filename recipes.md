# Recipes

Small jobs, whole. Each assumes the proxy
of chapter 4 and traffic that is yours
(chapter 1). Options are given for
mitmdump; the console and mitmweb take the
same options.

## See exactly what an app sends

The question behind half of this guide,
as a procedure:

```bash
mitmdump -p 8080 -w app-session.mitm
```

Point the app at the proxy — its settings
if it has them, its command-line proxy
option, or the environment:

```bash
http_proxy=http://127.0.0.1:8080 https_proxy=http://127.0.0.1:8080 the-app
```

Use the app. Stop the proxy. Read the file
at leisure (chapter 5), filtering first by
host (`~d`) and then by oddity — the
`~e` and non-200 flows are where the
secrets usually are.

## Record only the interesting part

A whole browsing session is mostly noise.
Filters work live as well as on files:

```bash
mitmdump -p 8080 -w api-only.mitm "~d api.example.com"
```

Only matching flows are written. The same
expression, on the `-w` line or in the
console's filter box, keeps a recording
small enough to read whole — and small
enough to share with a colleague without
leaking your other tabs (chapter 5's
warning, applied).

## Slow one route down

The poor-network test, as an addon
(chapter 9's hooks, one idea added — time):

```python
import time
from mitmproxy import http

def response(flow: http.HTTPFlow) -> None:
    if "/slow" in flow.request.path:
        time.sleep(2)
```

Save as `slow.py`, run with
`mitmdump -s slow.py`, and watch the
client cope with a two-second delay on
exactly the route you chose. Vary it:
sleep only sometimes, or kill one flow in
five (`flow.kill()`), and you have the
chaos shelf of client testing, in ten
lines you can read.

## A header that must not leave the house

Your own app is leaking a token to a
third-party endpoint you also use. Confirm
it in the capture (`~hs` searches the
responses; `~hq "Authorization"` finds the
requests carrying it), then decide whether
the fix belongs in the app (usually) — the
proxy's job here is the evidence, not the
bandage.

## Check a page's whole entourage

Set a browser's proxy to the lab
arrangement and load one page with
mitmweb open. The flow list is the page's
real supply chain: every tracker, font and
script, in the order they were fetched,
with sizes. Filter `~t image` or `~c 404`
to see the waste and the breakage. On your
own browsing, this is also the honest way
to learn what chapter 13 means by "not
everything is visible": what the page
fetched *before* you started the proxy, or
in a pinned app, simply is not there.

## Before-and-after for a fix

Record the failing session (recipe 1).
Fix the client. Replay the capture's
requests (chapter 10) or rerun the client
through a fresh recording, and read the
new file beside the old. Two recordings,
one variable changed: the closest thing
network debugging has to a controlled
experiment.
