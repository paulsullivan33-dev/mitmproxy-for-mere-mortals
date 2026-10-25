# Limits

What mitmproxy cannot do, and what it must
not be asked to do — the chapter the rest
of the guide has been promising.

## Some clients refuse, and they are right

**Certificate pinning.** A careful app
does not merely ask "is this certificate
signed by a trusted authority?" but "is
this *the* certificate, or one signed by
*my* authority?" Such an app meets
mitmproxy's minted certificate and refuses
— banking apps, payment apps, and
increasingly everything with something to
protect. There is no setting in mitmproxy
that changes this, by design on both
sides: the pin is the user of that app
being protected from exactly the seat this
guide occupies. Treat a refusal as
information (this app takes its channel
seriously), not as a lock to pick. On
your own apps you can of course unpin a
debug build; on other people's, the
refusal is the answer.

**Not everything is HTTP.** The proxy
reads HTTP and HTTPS (and WebSockets and
HTTP/2 riding on them). It does not decode
the binary protocol a game invented, the
sync chatter of a database, or DNS —
except by showing you the tunnel's
outside. Wireshark (chapter 12) is the
tool when the question is below HTTP.

**Not everything goes through proxies.**
Programs choose. Some ignore proxy
settings and environment variables, some
do their own DNS and pin their own
certificates, some — sandboxed and mobile
apps especially — live behind rules the
operating system enforces. A capture that
shows *nothing* about an app may be
chapter 14's empty capture (a setting)
or a true statement: this app's traffic
cannot be seated here. The other proxy
modes (chapter 2) exist for some of these
cases, each with its own privileges and
its own need for the chapter 1 rule.

## The CA is a liability you chose

Installing mitmproxy's CA into a machine's
trust store means: *anyone holding that
private key can present a valid-looking
certificate for any site to this machine.*
The key sits in a file in your home folder
(chapter 3), protected by your account's
permissions and nothing stronger. So:

- Install the CA only where you are
  actively using it; remove it when the
  work is done and the habit isn't.
- Never install it on a machine other
  people rely on without their knowing —
  a shared family computer counts.
- Guard `~/.mitmproxy` like a password
  file. If it may have leaked, delete it
  and let mitmproxy mint a new one; then
  remove the old CA from every trust
  store that took it.

## Recordings are liabilities too

A flow file is the traffic, whole:
passwords as typed, session cookies,
private content, the shape of a day's
browsing. Chapter 5 said keep them like
secrets; this is the same limit from the
other side. The proxy also *concentrates*
risk while it runs: a proxy left listening
on all interfaces (chapter 3's warning) is
an open relay with certificate-minting
ambitions, and on someone else's network
that is not a hobbyist's footprint.

## The legal and ethical edge

Chapter 1's rule — *your traffic, your
machines, or explicit permission* — is not
merely this guide being prim. Interception
of communications is regulated in most
jurisdictions (wiretapping and computer
misuse statutes in the US and Europe have
real teeth), workplace monitoring has its
own rules that belong to employers and
lawyers, and bypassing an app's pinning to
watch what it sends from an account that
is not yours is the fact pattern those
laws were written about. This guide is not
legal advice; it is a map edge that says,
in the plain style of the series: beyond
this line you are not debugging any more.
Everything inside the line — and it
encloses years of interesting, useful
work — needs no apology and no concealment.

## Performance and fidelity

A proxy is a hop. It adds latency, it is a
single point of failure for its clients,
and under real load (video, thousands of
flows) the console views get heavy. It
also changes what it touches more subtly:
connection reuse, ordering and timing are
the proxy's, not the original client's —
a fact the lab's transcripts show in the
`Proxy-Connection` header. For "what was
sent" that is no loss. For "why is it slow
at the packet level", it is the wrong
instrument — chapter 12's neighbours
again.
