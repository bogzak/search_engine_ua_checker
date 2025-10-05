from urllib.parse import urlparse
import argparse


def valid_url(url_value: str) -> str:
    vu = url_value.strip()
    parsed = urlparse(vu)
    if not parsed.scheme:
        vu = "https://" + vu
        parsed = urlparse(vu)
    if parsed.scheme.lower() not in ("http", "https") or not parsed.netloc:
        raise argparse.ArgumentTypeError("Invalid url")
    return vu


def mask_proxy(p: str) -> str:
    # http://user:pass@host:port -> http://***:***@host:port
    try:
        scheme, rest = p.split("//", 1)
        creds, host = rest.split("@", 1)
        if ":" in creds:
            return f"{scheme}://***:***@{host}"
    except ValueError:
        pass
    return p
