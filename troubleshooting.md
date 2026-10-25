# Troubleshooting

Symptom first, cause second, in the order
the lab and the documentation suggest you
check them.

## The capture is empty

*The proxy runs, the client works, and no
flows appear. The lab's own first hour.*

1. **The client bypassed the proxy for
   this address.** A `no_proxy` list (or a
   browser's "don't use the proxy for"
   setting) excludes local addresses on
   many machines, and curl honours it even
   with `-x` (chapter 4, transcript t90).
   Test: `curl -v` and read whether it
   connected to the proxy's port or the
   server's.
2. **The client was never told.** Proxy
   settings live per program, per profile,
   per environment. A new terminal does
   not inherit the variable you exported
   in another one.
3. **Wrong port or host.** The client
   points at 8080 on the machine you are
   *not* running mitmproxy on, or at a
   proxy that was stopped. `ss -tln` (or
   the startup line in mitmdump's output)
   shows who is actually listening.
4. **The app does not speak proxy.** Some
   programs ignore every setting (chapter
   13). Nothing is misconfigured; the seat
   is simply not on that road.

## The client reports a certificate error

*`curl: (60)`, a browser's warning page,
an app's flat refusal.*

1. **The CA is not trusted by this
   client** (chapter 8, the lab's second
   run). Each client has its own store:
   trusting the system store does nothing
   for a browser with a private one, and
   `--cacert` helps only that one command.
2. **Name mismatch.** The certificate is
   minted for the name in the URL. You
   asked for `127.0.0.1`; every certificate
   in sight says `localhost`. Use the name.
3. **The app pins its certificate**
   (chapter 13). No trust setting fixes
   this, and none should. The refusal is
   the diagnosis.
4. **Two CAs.** You deleted `~/.mitmproxy`
   (or use a second machine) and the client
   still trusts the *old* CA. Reinstall the
   current `mitmproxy-ca-cert.pem`.

## The proxy answers 502 for an HTTPS site

*The client trusted the CA, and still:*

```text
502 Bad Gateway
Certificate verify failed: self-signed certificate
```

That is chapter 8's first run: **mitmproxy**
could not verify the *server's*
certificate. On a lab server with a
home-made certificate this is expected,
and `--ssl-insecure` is the honest waiver
— for your server. On a real site, a 502
like this is a warning doing its job:
something between you and the site is
wrong, and the flag would only hide it.
For a server whose certificate is valid
but signed by a private CA (a company
one), point mitmproxy at that CA with
`--set ssl_verify_upstream_trusted_ca=…`
instead of waiving verification entirely.

## mitmweb says 403

You are at the right port without the
token (chapter 7). Copy the full address
from mitmweb's startup message, token and
all; it sets a cookie and the 403 becomes
the interface. If the startup message is
long gone, restart mitmweb — the token is
minted per run.

## Flows show a CONNECT and nothing inside

The client is tunnelling HTTPS but does
not trust the CA, so mitmproxy can only
relay the sealed tunnel — or the client
refused and the flow is the refusal. This
is the pre-chapter-8 state of the world,
not a fault: trust first (chapter 8), then
read.

## The addon does nothing

*No error, no effect.*

1. It was not loaded: `-s` names the file
   at startup; a running proxy does not
   notice the file appearing later. The
   startup output lists loaded addons.
2. It loaded and crashed quietly *once*:
   check the event log / console — an
   exception in a hook is reported there
   and the flow continues unmodified,
   which looks exactly like "nothing".
3. It worked, on traffic you were not
   watching: verify against the echo
   server (chapter 9's before/after), not
   against a site whose behaviour you are
   guessing at.

## The proxy is slow, or flows are missing pieces

Large downloads and streaming responses
are held, shown and forwarded like
everything else; a flow you read *while*
it is still streaming is a flow in
progress, not a truncated one. For very
large bodies, mitmproxy can stream rather
than buffer (the `stream_large_bodies`
option) — the trade is that addons then
see the body in pieces. And if the
*client* is slow only through the proxy,
remember chapter 13: the hop is real, and
on a busy machine the seat costs what it
costs.
