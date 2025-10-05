from typing import Optional
import requests
from fake_headers import Headers
from .models import ProbeResult


REDIRECT_CODES = {301, 302, 303, 307, 308}


def make_headers(custom_ua: str) -> dict:
    base = Headers(headers=True).generate()
    base["User-Agent"] = custom_ua
    return base

class HttpClient:
    def __init__(self, timeout: float = 3.0, proxies: Optional[dict] = None):
        self.session = requests.Session()
        self.timeout = timeout
        self.proxies = proxies

    def probe(self, url: str, engine: str, ua_name: str, ua_string: str, follow: bool) -> ProbeResult:
        headers = make_headers(ua_string)
        try:
            r = self.session.get(
                url,
                headers=headers,
                allow_redirects=False,
                timeout=self.timeout,
                proxies=self.proxies,
            )
            loc = r.headers.get("Location")
            final_url = None
            final_status = None

            if follow and (r.status_code in REDIRECT_CODES) and loc:
                # второй запрос идёт по Location
                r2 = self.session.get(
                    loc,
                    headers=headers,
                    allow_redirects=True,
                    timeout=self.timeout,
                    proxies=self.proxies,
                )
                final_url = r2.url
                final_status = r2.status_code

            return ProbeResult(
                engine=engine,
                ua_name=ua_name,
                ua_string=ua_string,
                initial_status=r.status_code,
                redirect_location=loc,
                final_url=final_url,
                final_status=final_status,
                error=None,
            )
        except requests.RequestException as e:
            return ProbeResult(
                engine=engine,
                ua_name=ua_name,
                ua_string=ua_string,
                initial_status=None,
                redirect_location=None,
                final_url=None,
                final_status=None,
                error=str(e),
            )
