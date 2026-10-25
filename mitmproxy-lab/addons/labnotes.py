"""A small mitmproxy addon for the lab.

It does two things, both easy to check against the echo server:

1. On the way out, it stamps every request with a header,
   X-Lab-Note. The echo server prints the headers it received,
   so the stamp shows up in the response body.

2. On the way back, it appends one line to plain-text
   responses, so a changed body is visible too.

Run it with:  mitmdump -s labnotes.py
"""

from mitmproxy import http


def request(flow: http.HTTPFlow) -> None:
    flow.request.headers["X-Lab-Note"] = "added-by-the-lab-addon"


def response(flow: http.HTTPFlow) -> None:
    flow.response.headers["X-Lab-Note"] = "answered-through-the-lab-addon"
    content_type = flow.response.headers.get("Content-Type", "")
    if content_type.startswith("text/plain"):
        flow.response.text = (
            flow.response.text + "[annotated by the lab addon]\n"
        )
