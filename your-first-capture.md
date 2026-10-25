# Your First Capture

The safest first capture is one where you
are the client, the server, and the person
in the middle — all three, on one machine.
Then nothing you record is anybody's
business but yours, and every surprise has
a local explanation. This chapter builds
that triangle and takes the capture the
rest of the guide keeps reading.

## A practice server

You need a server that answers on your own
machine and shows you what it received.
The lab wrote one for the purpose: a short
Python program, kept in this repository at
`mitmproxy-lab/server/echo_server.py`,
listening on port **18080** of the loopback
address. It answers every request with a
plain-text report — the method, the path,
every header, the body — so whatever a
request looked like when it *arrived* is
printed in the response. That honesty is
what later chapters cash in: when an addon
changes a request, the echo server says
so.

Start it in its own terminal:

```bash
python3 echo_server.py 18080
# echo-server listening on 127.0.0.1:18080
```

Any local server would do for a first
capture — `python3 -m http.server 18080`
serves files from a folder — but the echo
server's reports make the better teacher,
and it is the one in the transcripts.

## Pointing a client at the proxy

In a second terminal, start the proxy and
tell it to keep the flows:

```bash
mitmdump -p 8080 -w lab-http.mitm
```

`-p 8080` is the listening port (it is also
the default), and `-w` is the flow file of
chapter 2: every completed flow is written
there, to be read back in chapters 5, 6
and 10.

In a third terminal, make requests *through*
the proxy. curl takes its proxy per-request
with `-x`:

```bash
curl -s --noproxy '' -x http://127.0.0.1:8080 http://127.0.0.1:18080/hello
curl -s --noproxy '' -x http://127.0.0.1:8080 "http://127.0.0.1:18080/search?q=teapot&page=2"
curl -s --noproxy '' -x http://127.0.0.1:8080 -X POST -d "name=fern&soil=moist" http://127.0.0.1:18080/plants
curl -s --noproxy '' -o /dev/null -w "%{http_code}\n" -x http://127.0.0.1:8080 http://127.0.0.1:18080/missing
```

Four requests: a plain fetch, a search
with a query string, a small form post of
the kind a thousand web forms send, and a
page the echo server answers with an
honest **404**. Each response is the echo
server's report of what arrived. On the
proxy's terminal, mitmdump narrates the
same four journeys (transcript t01):

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

Stop mitmdump with Ctrl-C. The flow file
remains: the lab's was 8,388 bytes for
these four flows.

Check: you should be able to see, in the
echo server's first answer, a header the
direct request would not carry —
`Proxy-Connection: Keep-Alive`, added
because the request travelled the proxy
route. Small, but it is your first piece
of evidence that the middle seat is real.

## The trap this chapter exists to warn about

Every curl above carries `--noproxy ''`.
Here is why, from the lab's own stumble
(transcript t90). Many machines — servers
especially — have a **`no_proxy`
environment variable**: a list of addresses
that clients must *not* use a proxy for,
typically including `localhost` and
`127.0.0.1`, so that local traffic stays
local. curl honours that list **even when
you name a proxy explicitly with `-x`**:

```text
$ curl -v -x http://127.0.0.1:8080 http://127.0.0.1:18080/hello
* Uses proxy env variable no_proxy == 'localhost,127.0.0.1,::1,...'
* Connected to 127.0.0.1 (127.0.0.1) port 18080
> GET /hello HTTP/1.1
```

Read it closely: curl connected *directly*
to port 18080 and sent an ordinary request
(`GET /hello`, not the absolute URL a proxy
receives). The answers came back perfectly
— from the server, never passing the
proxy. mitmdump sat silent, its flow file
empty, looking exactly like a broken
install. It was not broken; it was
bypassed, politely, by a setting doing its
job.

The defences are the two commands you now
know: `--noproxy ''` empties the list for
that one curl, and `curl -v` *shows* the
decision when you suspect it. Other
programs have their own versions of this
list — browsers take proxy settings from
the system, and system settings often
exclude local addresses too. Chapter 14
returns to this under the heading it
deserves: *the empty capture*.

## What if the server is a real website?

It can be — your own traffic to a public
site is still your traffic. Start mitmdump
the same way, set your browser's proxy to
`127.0.0.1:8080`, and browse. Plain-HTTP
sites will record in full; HTTPS sites
will record as CONNECT tunnels whose
insides stay sealed until chapter 8's
certificate authority is trusted. Practise
on the echo server first anyway: when a
capture surprises you there, you can walk
to the other terminal and ask the server
what it saw.
