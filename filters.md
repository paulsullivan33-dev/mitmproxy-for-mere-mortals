# Filters

Four flows are a pleasure to read. Four
hundred are a haystack. mitmproxy's answer
is a small **filter language**: an
expression that says which flows you mean,
usable everywhere flows are listed —
reading a file, the console, mitmweb, and
several addon options. This chapter is the
language, exercised against the four flows
you already know (transcript t02 has every
run quoted here).

## The shape of a filter

A test is a tilde, a letter or two, and a
pattern:

```text
~m POST        the method is POST
~u search      the URL contains "search"
~c 404         the response status code is 404
```

Patterns are **regular expressions**,
matched anywhere in the target unless you
anchor them. Tests combine: `&` for *and*,
`|` for *or*, `!` for *not*, parentheses
for grouping.

## The tests worth memorising first

| Test | Matches flows whose… |
|---|---|
| `~u PATTERN` | URL matches |
| `~m METHOD` | request method is (GET, POST, …) |
| `~c CODE` | response status code is |
| `~s` | response exists (the request got an answer) |
| `~e` | flow ended in error |
| `~h PATTERN` | any header (request or response) matches |
| `~hq PATTERN` | request header matches |
| `~hs PATTERN` | response header matches |
| `~b PATTERN` | body (either side) contains |
| `~bq PATTERN` | request body contains |
| `~bs PATTERN` | response body contains |
| `~t TYPE` | content type contains (e.g. `~t json`) |
| `~d DOMAIN` | host matches |
| `~i` | flow is currently intercepted (console work) |

The full list is in the project's
documentation under "Filter expressions";
these dozen cover most days.

## Putting them to work

Filters ride along with `-r`. Only the
matching flows are processed — printed,
here, but the same selection drives
writing a smaller file or replaying a
subset (chapter 10):

```bash
$ mitmdump -nr lab-http.mitm "~m POST"
127.0.0.1:59878: POST http://127.0.0.1:18080/plants
              << 200 OK 257b

$ mitmdump -nr lab-http.mitm "~c 404"
127.0.0.1:59888: GET http://127.0.0.1:18080/missing
              << 404 Not Found 166b

$ mitmdump -nr lab-http.mitm "~u search & ~c 200"
127.0.0.1:59866: GET http://127.0.0.1:18080/search?q=teapot&page=2
              << 200 OK 181b
```

mitmdump announces the arrangement —
*Only processing flows that match…* — so a
filter that matched nothing looks
different from an empty file: the
announcement prints, then silence. When a
filter surprises you, widen before you
doubt: `~m post` in lower case matches
nothing, because methods on the wire are
upper case and matching is literal about
it.

Three habits separate pleasant filtering
from flailing:

- **Start from a flow you can see.** Pick
  the odd one in the list, then build the
  filter that selects exactly it. You have
  just written a description of the thing
  you were looking at.
- **Filter by the answer, not the
  question.** Errors cluster: `~c 404`,
  `~e`, `! ~s` (no response at all) pull
  the failures out of a big file faster
  than any URL pattern.
- **Bodies are the deep end.** `~b token`
  searches request *and* response bodies —
  the way to find which flow carried a
  particular value (a user name, an error
  string, the word a page should not
  contain) through a long session.

Check: against the lab's file,
`~bq "soil"` selects exactly the POST —
the only flow whose *request* body
contains the word — while `~bs "moist"`
selects it too, by its echo. One flow,
two roads in; on a real capture the roads
diverge, and knowing which side of the
conversation you are searching is the
whole skill.
