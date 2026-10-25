# Installing mitmproxy

mitmproxy is a Python program, and it is
installed the ways Python programs are:
from an operating system's packages, from
a standalone installer, or with pip. This
guide's lab used pip into a **virtual
environment** — a private folder holding
the program and its libraries, so the
install touches nothing else on the
machine and can be deleted by deleting the
folder. That is the route taught here;
the project's own standalone installers
(a single download for Windows, macOS and
Linux) are the alternative the official
documentation recommends for people who do
not live in Python, and they end at the
same three commands.

## The pip install

You need Python 3.10 or newer. On a Debian
or Ubuntu machine:

```bash
sudo apt install python3 python3-venv
python3 -m venv ~/mitm-venv
~/mitm-venv/bin/pip install mitmproxy
~/mitm-venv/bin/mitmproxy --version
```

On Windows and macOS the same pip route
works from a terminal with Python
installed, though most readers there will
prefer the standalone installer, which
also puts the commands on the path. In
the venv route, the three faces live in
the venv's `bin` folder (`Scripts` on
Windows); either call them by their full
path, or activate the environment first
with `source ~/mitm-venv/bin/activate`,
after which plain `mitmproxy`, `mitmdump`
and `mitmweb` are on the path for that
terminal.

Check: the lab's version printout
(transcript `mitmproxy-lab/transcripts/t00-version.txt`)
reads:

```text
$ mitmproxy --version
Mitmproxy: 12.3.0
Python:    3.12.3
OpenSSL:   OpenSSL 4.0.3 29 Sep 2026
```

The version matters when you read other
people's advice: mitmproxy is actively
developed, options move, and a tip written
for version 9 may name flags that version
12 has renamed. This guide's transcripts
are all from 12.3.0.

## The first run, and the folder it makes

Start any of the three faces once —

```bash
mitmdump -p 8080
```

— and stop it with Ctrl-C. Two things have
happened. The proxy listened on port 8080
(and would have answered had anything
connected). And in your home folder there
is now a new directory, **`~/.mitmproxy`**:

```text
$ ls ~/.mitmproxy/
mitmproxy-ca-cert.cer
mitmproxy-ca-cert.p12
mitmproxy-ca-cert.pem
mitmproxy-ca.p12
mitmproxy-ca.pem
mitmproxy-dhparam.pem
```

(from transcript t06). These files are
the certificate authority of chapter 2,
in several formats for several operating
systems:

| File | What it is |
|---|---|
| `mitmproxy-ca.pem` | The CA's certificate **and private key** together — the crown jewels |
| `mitmproxy-ca-cert.pem` | The certificate alone, PEM format (Linux, macOS, most tools) |
| `mitmproxy-ca-cert.cer` | The certificate alone, DER format (Windows double-click installs) |
| `mitmproxy-ca-cert.p12` / `mitmproxy-ca.p12` | The same material in PKCS#12 bundles, for browsers and phones that ask for them |
| `mitmproxy-dhparam.pem` | Diffie-Hellman parameters, a TLS detail you can leave alone |

The lab inspected its CA certificate
(transcript t06):

```text
$ openssl x509 -in ~/.mitmproxy/mitmproxy-ca-cert.pem -noout -subject -issuer
subject=CN = mitmproxy, O = mitmproxy
issuer=CN = mitmproxy, O = mitmproxy
```

Subject equals issuer: it signed itself,
which is what a root authority is. Nothing
on the internet trusts this CA. It becomes
powerful only on machines where someone —
you, chapter 8 — deliberately installs it
as trusted. Until then it is inert files,
and the proxy can still do everything in
chapters 4–7 with plain HTTP.

**Handle the folder like a key, because
it is one.** Do not mail it around, do not
commit it to a repository, do not copy it
onto machines you do not control. Chapter
13 explains what a stolen CA key buys an
attacker. If the folder is ever in doubt,
delete it: mitmproxy mints a fresh CA on
the next run, and you re-trust the new one
where you had trusted the old.

## Where the commands listen

By default the proxy listens on **every**
network interface at port 8080 — meaning a
mitmproxy left running on a laptop in a
café is, for a while, a proxy anyone on
that network can use, and can ask to mint
certificates. Two habits follow. Prefer
binding to the machine itself while you
learn: `--listen-host 127.0.0.1`. And stop
the proxy when you are done; a forgotten
proxy is an open door with your name on
it. mitmweb adds its own web port (8081
by default) and its own protection — a
one-time token in its startup address —
which chapter 7 shows working.
