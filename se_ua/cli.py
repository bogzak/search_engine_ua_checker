import argparse
import logging
from typing import List, Optional

from .ua_loader import load_user_agents
from .validators import valid_url, mask_proxy
from .http_client import HttpClient
from .runner import run_probes
from .output import print_results


DEFAULT_JSON = "user_agents.json"


def build_parser(engines: List[str]) -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="ua-probe",
        description="Check URL responses by emulating selected search-engine User-Agents.",
    )
    p.add_argument(
        "url", type=valid_url,
        help="URL to check (domain w/o scheme allowed)"
    )
    p.add_argument(
        "-e", "--engine", choices=engines, nargs="+", default=engines,
        help="Which engines to emulate (multiple allowed). Default: all."
    )
    p.add_argument(
        "--ua-json", default=DEFAULT_JSON,
        help=f"Path to UA JSON. Default: {DEFAULT_JSON}"
    )
    p.add_argument(
        "--proxy", metavar="URL",
        help="HTTP/HTTPS proxy, e.g. http://user:pass@host:port"
    )
    p.add_argument(
        "--timeout", type=float, default=3.0,
        help="Request timeout in seconds (default: 3.0)"
    )
    p.add_argument(
        "--follow", action="store_true", default=True,
        help="Follow one redirect (uses Location)"
    )
    p.add_argument(
        "--concurrency", type=int, default=4,
        help="Parallel requests (default: 4)"
    )
    p.add_argument(
        "--out", choices=["human", "json"], default="human",
        help="Output format (default: human)"
    )
    p.add_argument(
        "-v", "--verbose", action="count", default=0,
        help="Increase verbosity (-v, -vv)"
    )
    return p


def setup_logging(verbosity: int) -> None:
    level = logging.WARNING
    if verbosity == 1:
        level = logging.INFO
    elif verbosity >= 2:
        level = logging.DEBUG
    logging.basicConfig(level=level, format="%(levelname)s: %(message)s")


def main(argv: Optional[List[str]] = None) -> None:
    ua_map = load_user_agents(DEFAULT_JSON)
    engines = sorted(ua_map.keys())

    parser = build_parser(engines)
    args = parser.parse_args(argv)

    setup_logging(args.verbose)

    if args.ua_json != DEFAULT_JSON:
        ua_map = load_user_agents(args.ua_json)
        engines = sorted(ua_map.keys())
        if args.engine == parser.get_default("engine"):
            args.engine = engines

    proxies = {"http": args.proxy, "https": args.proxy} if args.proxy else None

    logging.info("URL: %s", args.url)
    if args.proxy:
        logging.info("Proxy: %s", mask_proxy(args.proxy))
    logging.info("Engines: %s", ", ".join(args.engine))

    client = HttpClient(timeout=args.timeout, proxies=proxies)

    results = run_probes(
        client=client,
        url=args.url,
        ua_map=ua_map,
        engines=args.engine,
        follow=args.follow,
        concurrency=max(1, args.concurrency),
    )

    print_results(results, out=args.out)
