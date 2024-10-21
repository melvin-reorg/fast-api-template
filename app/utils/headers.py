"""This module contains the default headers that will be injected in the response of the API."""

from fastapi import Response


def default_headers_injection(response: Response):
    response.headers["Cache-control"] = "no-cache"
    response.headers["Strict-Transport-Security"] = (
        "max-age=63072000; includeSubDomains; preload"
    )
    response.headers["Pragma"] = "no-cache"
    response.headers["X-Frame-Options"] = "Deny"
    response.headers["Content-Security-Policy"] = (
        "default-src 'none'; img-src 'self'; script-scr 'self'; style-src 'self'; object-src 'none'"
    )
