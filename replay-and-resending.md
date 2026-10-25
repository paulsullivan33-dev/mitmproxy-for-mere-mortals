# Replay and Resending

A flow file is not only for reading. Its
requests can be **sent again** — at the
same server, at a test server, tomorrow,
after you change something — and the new
answers compared with the recorded ones.
That turns a capture from a photograph
into a repeatable experiment, and it is
the last of the core skills this guide
teaches.

## Client replay

`mitmdump -C` (for *client* replay) reads a
flow file and issues each recorded request
again, as if the original client had come
back (transcript t07):

```text
$ mitmdump -C flows/lab-http.mitm
[replay]: GET http://127.0.0.1:18080/hello
              << 200 OK 164b
[replay]: GET http://127.0.0.1:18080/search?q=teapot&page=2
              << 200 OK 181b
[replay]: POST http://127.0.0.1:18080/plants
              << 200 OK 257b
[replay]: GET http://127.0.0.1:18080/missing
              << 404 Not Found 166b
```

All four of chapter 4's requests went out
a second time and were answered exactly as
before — the same sizes, the same 404 —
because the echo server has no memory and
the world had not changed. That sameness
is the baseline; replay earns its keep
when something *has* changed:

- **A new version of the server.** Record
  against the old one, replay against the
  new, and diff the two sets of responses.
  Every difference is a question with a
  name.
- **A client bug, revisited.** The failing
  request from a bug report is in the
  capture; replay it all afternoon while
  you fix, instead of coaxing the original
  program into failing again on cue.
- **Load, modestly.** Replay with several
  flows in parallel (`--replay-*` options
  and the console's `r` key cover the
  mechanics) gives a small, honest
  rehearsal — not a load test: a proxy is
  a hop, not a harness (chapter 13).

Filters (chapter 6) apply here too: a
filter expression with `-C` replays only
the matching requests, so the one failing
call in a four-hundred-flow file goes out
alone.

## Server replay, and the difference

There is a second direction. `mitmdump -S`
(*server* replay) answers *incoming*
requests from a flow file instead of
fetching them: a client talks to the
proxy, and the proxy replies with the
recorded response for a matching request,
never troubling a real server. That is a
recording used as a **mock** — the client
under development believes the API is up;
in fact last Tuesday's answers are being
served from a file. The lab did not run
server replay (its echo server was always
awake), so it is taught here from the
documentation and logged in `criteria.md`
as documented-only. Between the two:
client replay repeats the *questions*,
server replay repeats the *answers*.

## What replay cannot prove

A replayed request is a new request. The
server may have state — a session, a
counter, a clock — and a request that
depends on it (a second page fetched with
a token from the first) may fail or, more
treacherously, succeed differently. Treat
a replay mismatch as a *lead*, not a
verdict: it tells you where to look, not
what happened. And one more restraint, from
chapter 1: replay sends real requests to
real servers. Replaying your own capture
against your own server is a rehearsal;
replaying a capture that contains someone
else's session tokens, at a service you do
not run, is using credentials that are not
yours. The file makes it easy; the rule
still decides.
