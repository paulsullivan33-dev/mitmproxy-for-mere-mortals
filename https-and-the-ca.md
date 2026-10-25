# HTTPS and the Certificate Authority

Everything so far was plain HTTP — text
anyone on the path could read anyway.
Real traffic is **HTTPS**: the conversation
is encrypted between client and server, and
a seat in the middle should see nothing
but noise. This chapter explains how
mitmproxy reads it anyway — not by breaking
the encryption, but by being *invited
inside* it — and the lab proves each step
against the echo server, wearing a
self-made certificate.

## Two conversations pretending to be one

When a client asks the proxy for
`https://localhost:18443/diary`, the
exchange (called a CONNECT tunnel) goes
like this:

1. The client opens an encrypted
   connection **to mitmproxy**, believing
   it is talking to `localhost`. For that
   belief to survive, mitmproxy must show
   a certificate for the name `localhost`
   that the client accepts. It mints one
   on the spot, signed by its own CA
   (chapter 3).
2. mitmproxy separately opens an encrypted
   connection **to the real server**,
   checks *its* certificate the way any
   client would, and relays.
3. The client encrypts with keys it shares
   with mitmproxy; mitmproxy decrypts,
   records the flow **in clear**, and
   re-encrypts toward the server.

No mathematics is harmed. The whole trick
stands on step 1's *if*: the client must
**trust mitmproxy's CA**. Without that
trust the client looks at the minted
certificate, sees an unknown signer, and
refuses — correctly. With it, the padlock
in a browser still shows, because as far
as the client's rules are concerned, a
trusted authority vouched for the
certificate. *That* is why chapter 3
called the CA folder a loaded key, and why
installing it is a decision, not a setup
detail.

## Teaching a client to trust the CA

How trust is installed depends on the
client:

- **A single command-line tool:** point it
  at the certificate file. curl takes
  `--cacert ~/.mitmproxy/mitmproxy-ca-cert.pem`;
  most tools have an equivalent. This is
  the narrowest trust — one program, one
  run if you like — and it is what the lab
  used.
- **A browser:** browsers keep their own
  or the system's trust store. mitmproxy
  offers a shortcut: with the proxy set,
  visit **mitm.it** in that browser and it
  serves the CA certificate for your
  platform with install instructions.
- **An operating system:** installing the
  `.cer`/`.pem` into the system store
  makes *every* program that uses it trust
  the CA. Widest trust, widest blast
  radius if the key leaks.
- **Other devices** (a phone you own):
  the same mitm.it route over the network.
  The lab had no second device, so this
  guide describes the mechanism and does
  not pretend to have walked a phone
  through it — `criteria.md` logs it as
  documented-only.

## The lab: three answers, in order

The echo server put on TLS: the lab made
it a self-signed certificate (its own
one-line authority, `CN=localhost`) and
started it on port 18443 (transcript t04).
Then three runs taught the whole chapter.

**First, the proxy refuses the server.**
With mitmproxy's defaults, even a client
that trusted the CA got:

```text
502 Bad Gateway
Certificate verify failed: self-signed certificate
```

mitmproxy checks the *server's*
certificate as strictly as any client
should, and the lab's home-made certificate
fails — as, on the open internet, a
forgery would. The flag `--ssl-insecure`
tells mitmproxy to accept server
certificates it cannot verify. The lab
used it from here on, for its own server,
knowing exactly which check it was
switching off. On real traffic, reaching
for that flag should feel like what it is:
agreeing not to know who answered.

**Second, the client refuses the proxy.**
With the proxy now willing, a client that
did *not* trust the CA met:

```text
curl: (60) SSL certificate problem: unable to get local issuer certificate
```

curl was shown a certificate for
`localhost` signed by an authority it had
never heard of, and stopped. This refusal
is the internet's immune system working;
chapter 13 meets apps that refuse the same
way and cannot be argued with.

**Third, with trust, the middle reads
everything.** curl, given
`--cacert ~/.mitmproxy/mitmproxy-ca-cert.pem`,
posted a small secret to the diary page:

```bash
curl -s --cacert ~/.mitmproxy/mitmproxy-ca-cert.pem \
     -x http://127.0.0.1:8080 \
     -X POST -d "note=the-eagle-flies-at-dawn" \
     https://localhost:18443/diary
```

The server answered happily — its echo
showed the note had arrived. And the flow
file, read back afterwards, held the whole
encrypted conversation **in clear text**
(transcript t04):

```text
127.0.0.1:57454: POST https://localhost:18443/diary
    ...
    note: the-eagle-flies-at-dawn
 << 200 OK 233b
    ...
    body:
    note=the-eagle-flies-at-dawn
```

Contemplate that for a moment, because it
is the chapter: the encryption was never
broken, never weakened, and both endpoints
behaved correctly throughout. The
difference was one trust decision. That is
why the CA belongs on machines you own,
for traffic that is yours (chapter 1's
rule), and why a "free certificate" anyone
offers you for a device you care about
should make the hair on your neck stand
up.

## A note on names

mitmproxy mints the certificate for the
name the client asked for — which is why
the lab's client said `localhost` and not
`127.0.0.1`: the server's real certificate
and the minted one must both match the
name in the URL. Asking for an address the
certificate does not cover produces the
other classic certificate error, a name
mismatch, and chapter 14 keeps it in the
catalogue.
