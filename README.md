# Search engine User-agent checker

Emulate search-engine User-Agents and inspect how a website responds: status codes, redirects, and final destinations — fast and scriptable.

## Features
- 🔁 Test multiple engines / multiple UAs per engine
- 🧠 Sensible URL validation (example.com → https://example.com)
- 🧵 Concurrent requests (--concurrency)
-  Proxy support
- 🧷 Optional one-hop redirect follow (uses Location)
- 🙂 Emoji hints for status families (1xx..5xx)
- 📤 Human or JSON output (great for CI)

## Installation

```bash
git clone <your-repo-url>
cd <your-repo-directory>
uv sync
```

## Quickstart

```bash
# Basic usage
uv run main.py example.com
# Specify search engines
uv run main.py example.com --engines google bing
# Run with proxy
uv run main.py example.com --proxy http://user:pass@host:8080
# JSON output
uv run main.py example.com --json > report.json
# Show help
uv run main.py -h

```

## CLI options
```text
usage: se_ua [-h] [-e {…} [{…} ...]] [--ua-json PATH] [--proxy URL]
                [--timeout SECONDS] [--follow] [--concurrency N]
                [--out {human,json}] [-v] [--version]
                url
```

### Arguments
- `url`: The target URL to test (e.g., example.com or https://example.com).
- '-e', '--engines': Specify which search engines to emulate. Default: all supported engines.
- `--ua-json PATH`: Path to a JSON file with custom User-Agent strings.
- `--proxy URL`: Use a proxy for requests (e.g., http://user:pass@host:port).
- `--timeout SECONDS`: Set request timeout in seconds (default: 3.0).
- `--follow`: Follow one redirect (default=True).
- `--concurrency N`: Number of concurrent requests (default: 4).
- `--out {human,json}`: Output format (default: human).
- `-v`, `-vv`: Enable verbose output.

## Output (human)
```yaml
[google] Googlebot Smartphone
UA: Mozilla/5.0 (...)
Status: 302 🔀
Redirect: https://m.example.com/
Final URL: https://m.example.com/
Final Status: 200 ✅
--------------------------------------------------------------------------------
```
### Status emoji map
`1xx` ℹ️ `2xx` ✅ `3xx` 🔀 `4xx` ⛔ `5xx` 💥

## Output (JSON)
```json
[
  {
    "engine": "google",
    "ua_name": "Googlebot Smartphone",
    "ua_string": "Mozilla/5.0 (...)",
    "initial_status": 302,
    "redirect_location": "https://m.example.com/",
    "final_url": "https://m.example.com/",
    "final_status": 200,
    "error": null
  }
]

```

## Contributing
Contributions are welcome! Please open issues or pull requests for bugs, features, or improvements.

## License
This project is licensed under the MIT License.