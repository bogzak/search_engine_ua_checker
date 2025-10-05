from dataclasses import dataclass
from typing import Optional

@dataclass
class ProbeResult:
    engine: str
    ua_name: str
    ua_string: str
    initial_status: Optional[int]
    redirect_location: Optional[str]
    final_url: Optional[str]
    final_status: Optional[int]
    error: Optional[str]
