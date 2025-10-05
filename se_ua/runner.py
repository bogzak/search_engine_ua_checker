from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, Iterable, List, Tuple
from .models import ProbeResult
from .http_client import HttpClient


def iter_selected_pairs(
    ua_map: Dict[str, List[Tuple[str, str]]],
    engines: Iterable[str],
) -> Iterable[tuple[str, str, str]]:
    for engine in engines:
        pairs = ua_map.get(engine, [])
        for (ua_name, ua_string) in pairs:
            yield engine, ua_name, ua_string


def run_probes(
    client: HttpClient,
    url: str,
    ua_map: Dict[str, List[Tuple[str, str]]],
    engines: List[str],
    follow: bool,
    concurrency: int,
) -> List[ProbeResult]:
    tasks = list(iter_selected_pairs(ua_map, engines))
    results: List[ProbeResult] = []

    if concurrency <= 1:
        for engine, ua_name, ua_string in tasks:
            results.append(client.probe(url, engine, ua_name, ua_string, follow))
        return results

    with ThreadPoolExecutor(max_workers=concurrency) as pool:
        futs = [
            pool.submit(client.probe, url, engine, ua_name, ua_string, follow)
            for engine, ua_name, ua_string in tasks
        ]
        for f in as_completed(futs):
            results.append(f.result())
    return results
