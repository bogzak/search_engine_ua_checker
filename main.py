from random import choices
from typing import Optional
from urllib.parse import urlparse

import requests
import json
import argparse


JSON_FILE = "user_agents.json"
REDIRECT_CODES = {301, 302, 303, 307, 308}


def valid_url(url_value: str) -> str:
    parsed = urlparse(url_value)
    if parsed.scheme not in ["http", "https"] or not parsed.netloc:
        raise argparse.ArgumentTypeError("Invalid url")
    return url_value


def load_user_agents(path: str) -> dict:
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError as e:
        raise SystemExit(f"File with User-Agent not found: {path}") from e
    except json.JSONDecodeError as e:
        raise SystemExit(f"Invalid JSON in {path}: {e}") from e

    norm = {}
    for engine, mapping in data.items():
        eng = str(engine).lower().strip()
        if isinstance(mapping, dict):
            norm[eng] = [ua for ua in mapping.values()]
        if isinstance(mapping, list):
            norm[eng] = [ua for ua in mapping]
        if isinstance(mapping, str):
            norm[eng] = [mapping]
        else:
            norm[eng] = []
    return norm


def build_parser(engines):
    parser = argparse.ArgumentParser(
        description="Checks the URL response by substituting the User-Agent of selected search engines."
    )
    parser.add_argument(
        "url",
        type=valid_url,
        help="The URL to check",
    )
    parser.add_argument(
        "-e", "--engine",
        choices=engines,
        nargs="+",
        default=engines,
        help=f"Which engines to emulate (multiple selections possible): {choices}. All by default."
    )
    parser.add_argument(
        "--proxy",
        metavar="URL",
        help="HTTP/HTTPS proxy, for example http://user:pass@host:port",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=1.0,
        help="How long to wait for each request (in seconds)",
    )
    return parser


def request_once(
        session: requests.Session,
        url: str,
        user_agent: str,
        timeout: float,
        proxies: Optional[dict],
):
    headers = {"User-Agent": user_agent}

    resp = session.get(
        url,
        headers=headers,
        allow_redirects=False,
        timeout=timeout,
        proxies=proxies
    )
    print(f"Status: {resp.status_code}")
    if resp.status_code in REDIRECT_CODES:
        loc = resp.headers.get("Location")
        print(f"Redirect: {loc}")

        try:
            final = session.get(
                url,
                headers=headers,
                allow_redirects=True,
                timeout=timeout,
                proxies=proxies,
            )
            print(f"Final URL: {final.url}")
            print(f"Final Status: {final.status_code}")
        except requests.RequestException as e:
            print(f"Error during redirect: {e}")


def main():
    ua_map = load_user_agents(JSON_FILE)
    engines = sorted(ua_map.keys())

    parser = build_parser(engines)
    args = parser.parse_args()

    proxies = {
        "http": args.proxy,
        "https": args.proxy,
    } if args.proxy else None

    print(f"URL: {args.url}")
    if args.proxy:
        print(f"Proxy: {args.proxy}")
    print(f"Engines: {', '.join(args.engine)}")
    print("-" * 80)

    session = requests.Session()

    for engine in args.engine:
        uas = ua_map.get(engine, [])
        if not uas:
            print(f"[{engine}] No User-Agent found for {args.url}")
            print("-" * 80)
            continue

        for idx, ua in enumerate(uas, start=1):
            print(f"[{engine}] [{idx}] {ua}")
            try:
                request_once(session, args.url, ua, args.timeout, proxies=proxies)
            except requests.exceptions.ConnectionError as e:
                print(f"Connection error: {e}")
            except requests.RequestException as e:
                print(f"Request error: {e}")
            print("-" * 80)


if __name__ == "__main__":
    main()
