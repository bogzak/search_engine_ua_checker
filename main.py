from random import choices
from urllib.parse import urlparse

import requests
import json
import argparse


JSON_FILE = "user_agent_search_test.json"
SE = ["google", "yandex", "bing"]


with open(JSON_FILE) as f:
    se_json = json.load(f)


def valid_url(url_value: str) -> str:
    parsed = urlparse(url_value)
    if parsed.scheme not in ["http", "https"] or not parsed.netloc:
        raise argparse.ArgumentTypeError("invalid url")
    return url_value


def build_parser():
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
        choices=SE,
        nargs="+",
        default=SE,
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


def main():
    args = build_parser().parse_args()
    for user_agent in SE:
        headers = {"User-Agent": user_agent}
        try:
            response = requests.get(args.url, headers=headers, allow_redirects=False, timeout=10)
            print(f"User-Agent: {user_agent}")
            print(f"Status Code: {response.status_code}")
            if response.status_code in [301, 302]:
                print(f"Start URL: {response.url}")
                try:
                    response_3xx = requests.get(args.url, headers=headers, allow_redirects=True, timeout=10)
                    print(f"Final URL: {response_3xx.url}")
                except requests.exceptions.RequestException as e:
                    print(f"Error on redirect: {e}")
            print("-" * 80)
        except requests.exceptions.ConnectionError as e:
            print(f"User-Agent: {user_agent}")
            print(f"Connection error: {e}")
            print("-" * 80)
        except requests.exceptions.RequestException as e:
            print(f"User-Agent: {user_agent}")
            print(f"Request error: {e}")
            print("-" * 80)

if __name__ == "__main__":
    main()
