import json
from typing import Iterable, Literal, List
from .models import ProbeResult
from .status_emoji import StatusEmoji


def print_human(results: Iterable[ProbeResult], status_emoji: StatusEmoji) -> None:
    for res in results:
        print(f"[{res.engine}] {res.ua_name}")
        print(f"UA: {res.ua_string}")
        if res.error:
            print(f"Error: {res.error}")
        else:
            em = status_emoji(res.initial_status) if res.initial_status is not None else "❓"
            print(f"Status: {res.initial_status} {em}")
            if res.redirect_location:
                print(f"Redirect: {res.redirect_location}")
            if res.final_status is not None:
                em2 = status_emoji(res.final_status)
                print(f"Final URL: {res.final_url}")
                print(f"Final Status: {res.final_status} {em2}")
        print("-" * 80)

def to_json(results: Iterable[ProbeResult]) -> str:
    def _asdict(r: ProbeResult):
        return {
            "engine": r.engine,
            "ua_name": r.ua_name,
            "ua_string": r.ua_string,
            "initial_status": r.initial_status,
            "redirect_location": r.redirect_location,
            "final_url": r.final_url,
            "final_status": r.final_status,
            "error": r.error,
        }
    return json.dumps([_asdict(r) for r in results], ensure_ascii=False, indent=2)

def print_results(results: List[ProbeResult], out: Literal["human", "json"] = "human") -> None:
    if out == "json":
        print(to_json(results))
    else:
        print_human(results, StatusEmoji())
        