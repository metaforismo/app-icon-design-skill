#!/usr/bin/env python3
"""Check the curated official-source manifest and optionally emit JSON evidence."""

from __future__ import annotations

import argparse
import json
import urllib.error
import urllib.request
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "docs" / "source-manifest.yaml"


def load_manifest(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        raise ValueError("source manifest must use schema_version: 1")
    if not isinstance(data.get("verified_on"), str):
        raise ValueError("source manifest needs verified_on")
    sources = data.get("sources")
    if not isinstance(sources, list) or not sources:
        raise ValueError("source manifest must contain sources")
    required = {"id", "title", "authority", "area", "url"}
    identifiers: set[str] = set()
    for source in sources:
        if not isinstance(source, dict) or set(source) != required:
            raise ValueError("every source must contain id, title, authority, area, and url")
        if source["id"] in identifiers:
            raise ValueError(f"duplicate source id: {source['id']}")
        identifiers.add(source["id"])
        if source["authority"] != "Apple":
            raise ValueError(f"changing platform claims require primary Apple sources: {source['id']}")
        if not source["url"].startswith("https://developer.apple.com/"):
            raise ValueError(f"source is not an official Apple URL: {source['id']}")
    return data


def check_url(url: str, timeout: float) -> dict:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "app-icon-design-skill-source-check/1.0"},
        method="GET",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            status = response.status
            final_url = response.geturl()
    except urllib.error.HTTPError as exc:
        status = exc.code
        final_url = exc.geturl()
        error = str(exc)
    except urllib.error.URLError as exc:
        return {"url": url, "ok": False, "status": None, "final_url": None, "error": str(exc)}
    else:
        error = None
    return {
        "url": url,
        "ok": 200 <= status < 400,
        "status": status,
        "final_url": final_url,
        "error": error,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--timeout", type=float, default=20.0)
    args = parser.parse_args()

    manifest = load_manifest(args.manifest)
    results = []
    for source in manifest["sources"]:
        result = check_url(source["url"], args.timeout)
        result.update({"id": source["id"], "title": source["title"]})
        results.append(result)
        print(f"{'OK' if result['ok'] else 'FAIL'} {source['id']}: {result['status']} {result['final_url'] or source['url']}")

    report = {
        "manifest": str(args.manifest),
        "verified_on": manifest["verified_on"],
        "results": results,
        "passed": all(result["ok"] for result in results),
    }
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
