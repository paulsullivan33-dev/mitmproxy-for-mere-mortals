# Writing criteria for this guide

Every "for Mere Mortals" guide is written to the same nine-point
standard, so a reader who trusts one can trust the rest. Here it
is, with the verification notes for this particular guide below.

1. **Fix it first.** Reader outcomes lead, not action items: each
   chapter opens by naming the outcome it delivers, shows a check
   the reader can run to confirm they got it, and a reasonable
   reader finishes able to state what was done, what it means,
   and what to try next.
2. **Plain language.** Short sentences, everyday vocabulary,
   technical terms defined on first use. No slang, and no
   idioms that only make sense in one country — the reader may
   be translating as they go.
3. **No dead ends.** A guide never tells the reader to do
   something it cannot show them how to verify. Every claim a
   reader relies on — an install, a command, an output — is
   something this guide demonstrates or clearly labels
   documented-only below.
4. **Live-verified where it matters.** Procedures are run for
   real in the guide's lab wherever the build machine allows it,
   and the transcripts kept in the repository are the evidence.
   What could not be run is listed honestly below, never
   presented as if it had been.
5. **General audiences.** Nothing in this guide — examples,
   fixtures, names, addresses — is modelled on any particular
   reader or author's real life, network, or organisations.
   The lab's traffic is the lab talking to itself.
6. **Standalone.** A reader needs this guide, its lab, and
   nothing else. Where another guide would genuinely help, it
   is pointed to once, by name, and the chapter still completes
   without it.
7. **Honest about limits.** Chapter 13 names what the tool
   cannot do: clients that pin their certificates, traffic that
   is not HTTP, programs that never use a proxy, the CA as a
   liability, the recordings as secrets, and the legal edge
   around intercepting anything that is not yours.
8. **The ethics rule is in the text, early.** Chapter 1 and the
   README state the rule plainly — *your traffic, your
   machines, or explicit permission* — before any procedure
   depends on it, and later chapters point back to it where the
   tooling would make crossing the line easy.
9. **Builds clean.** The site builds with MkDocs in strict mode
   with no warnings, and a fresh reader following the chapters
   in order reaches the stated outcome of each.

## Verification notes for this guide

The build machine is a 2-CPU, 7.7 GB Ubuntu 24.04 sandbox.
mitmproxy **12.3.0** was installed with pip into a fresh virtual
environment (Python 3.12.3) and exercised against a throwaway
echo server written for this guide (`mitmproxy-lab/server/`),
running on loopback only. All transcripts live in
`mitmproxy-lab/transcripts/`; the addon from chapter 9 is
`mitmproxy-lab/addons/labnotes.py`.

Run for real, with transcripts as evidence:

- Install and version; first run generating the CA in
  `~/.mitmproxy`, and the CA certificate's subject, issuer and
  fingerprint read back with openssl (t00, t06).
- Four HTTP requests (GET, query-string GET, form POST, a 404)
  captured by `mitmdump -w` to a flow file, and the file read
  back with `-r` (t01, t02).
- The filter language on that capture: `~m`, `~c`, a combined
  `&` expression, `~bq`/`~bs` body searches, a `flow_detail=4`
  close read, and a filtered subset written to a new file and
  re-read (t02).
- A real addon that stamps a header onto requests and
  responses and annotates plain-text bodies, proven three ways:
  the echo server's report of what it received, the response
  headers and body seen by curl, and the recorded flow's sizes
  (t03).
- HTTPS interception end to end, against the echo server under
  a self-signed certificate made for the lab: mitmproxy's 502
  refusal of the unverifiable server certificate, curl's exit
  60 refusal when it did not trust mitmproxy's CA, and — with
  `--cacert` trust — the decrypted POST, body included, in the
  recorded flow (t04).
- mitmweb answering on its web port: 403 without its startup
  token, 200 with it, the interface title, and the `/flows`
  JSON endpoint returning the live flow (t05).
- Client replay (`mitmdump -C`): all four recorded requests
  re-sent and answered identically (t07).
- The lab's central trap, also run for real: the build
  machine's `no_proxy` made curl bypass the proxy despite an
  explicit `-x`, shown by `curl -v` connecting directly; every
  capture in the guide uses `--noproxy ''` to defeat it (t90).

Documented only — described from the project's documentation,
not run, and the text does not claim otherwise:

- The console interface's interactive keys (its flow data is
  the same verified flow model; a terminal UI leaves no
  transcript to keep).
- Pointing a second machine or a phone at the proxy, the
  mitm.it helper page, and installing the CA into an operating
  system's or browser's trust store (the lab exercised
  per-command trust only: curl `--cacert`).
- Reverse, transparent, WireGuard and local-capture modes,
  which need network privileges the sandbox does not grant.
- Server replay (`mitmdump -S`); client replay was run and is
  the verified half of chapter 10.
- Certificate pinning as experienced on real third-party apps;
  the lab's curl exit-60 refusal is the same mechanism's first
  cousin, and chapter 13 says exactly that.
- The comparison tools in chapter 12 are characterised, not
  benchmarked.

Fixtures are this guide's own and deliberately generic: a
twenty-line echo server that reports what it receives, an
addon that stamps its own name on traffic, and one invented
sentence of "secret" data sent by the lab to itself. No
example is modelled on any real person, network, service or
organisation, and nothing was intercepted that the lab did not
itself originate.
