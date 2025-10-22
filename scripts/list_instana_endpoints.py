# ...existing code...
import json
import os
import requests
from urllib.parse import urljoin
from typing import Dict, Any, List

CONF = ".vscode/mcp.json"
OUT = "instana_endpoints.json"

CANDIDATE_PATHS: List[str] = [
    "/api/0/applications",
    "/api/0/services",
    "/api/0/endpoints",
    "/api/0/hosts",
    "/api/0/agents",
    "/api/0/resources",
    "/api/application-monitoring/applications",
    "/api/application-monitoring/endpoints",
    "/api/application-monitoring/services",
    "/api/application-monitoring/metrics",
    "/api/application-monitoring/spans",
    "/api/endpoints",
    "/api/v1/endpoints",
    "/api/v1/services",
    "/api/v1/applications",
    "/api/v1/hosts",
    "/api/v2/endpoints",
    "/api/v2/services",
    "/api/v2/applications",
    "/api",
    "/api/status",
]


def load_config(path: str = CONF) -> tuple[str, str]:
    """
    Load INSTANA_BASE_URL and INSTANA_API_TOKEN from .vscode/mcp.json
    Returns (base_url, api_token)
    """
    with open(path, "r", encoding="utf-8") as fh:
        cfg = json.load(fh)
    srv = cfg.get("servers", {}).get("Instana MCP Server", {})
    env = srv.get("env", {})
    base = env.get("INSTANA_BASE_URL")
    token = env.get("INSTANA_API_TOKEN")
    if not base or not token:
        raise SystemExit(f"Missing INSTANA_BASE_URL or INSTANA_API_TOKEN in {path}")
    return base.rstrip("/"), token


def probe(base_url: str, token: str, candidates: List[str]) -> Dict[str, Any]:
    """
    Probe candidate paths and return a mapping of path -> result dict
    """
    headers = {"Authorization": f"apiToken {token}", "Accept": "application/json"}
    results: Dict[str, Any] = {}
    session = requests.Session()
    session.headers.update(headers)
    for path in candidates:
        url = urljoin(base_url + "/", path.lstrip("/"))
        try:
            r = session.get(url, timeout=15, verify=True)
        except Exception as e:
            results[path] = {"url": url, "error": str(e)}
            continue
        # try to parse json, otherwise keep text (truncated)
        try:
            body = r.json()
        except ValueError:
            body = r.text[:2048]
        results[path] = {"url": url, "status_code": r.status_code, "body": body}
    return results


def main():
    base, token = load_config()
    print("Probing Instana at", base)
    res = probe(base, token, CANDIDATE_PATHS)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=2, ensure_ascii=False)
    successes = [p for p, v in res.items() if v.get("status_code") == 200]
    print("Successful endpoints (HTTP 200):")
    for p in successes:
        print(" -", p, "->", res[p]["url"])
    print(f"Full probe results written to ./{OUT}")


if __name__ == "__main__":
    main()