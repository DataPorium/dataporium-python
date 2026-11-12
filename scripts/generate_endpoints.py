"""Rebuild dataporium/endpoints.json and docs/endpoints.md from the public OpenAPI file.

Usage:
    python scripts/generate_endpoints.py            # downloads https://dataporium.tech/openapi.json
    python scripts/generate_endpoints.py spec.json  # uses a local copy
"""
from __future__ import annotations

import json
import sys
import urllib.request
from pathlib import Path

SPEC_URL = "https://dataporium.tech/openapi.json"
ROOT = Path(__file__).resolve().parent.parent


def load_spec(argv: list[str]) -> dict:
    if len(argv) > 1:
        return json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    with urllib.request.urlopen(SPEC_URL, timeout=60) as resp:  # noqa: S310
        return json.loads(resp.read().decode("utf-8"))


def clean(text: str | None) -> str:
    return " ".join((text or "").split())


def build(spec: dict) -> dict:
    endpoints = {}
    for path, operations in spec["paths"].items():
        op = operations.get("get")
        if not op:
            continue
        name = op["operationId"]
        params = []
        for p in op.get("parameters", []):
            item = {"name": p["name"], "in": p.get("in", "query"), "description": clean(p.get("description"))}
            if p.get("example") is not None:
                item["example"] = p["example"]
            params.append(item)
        endpoints[name] = {
            "path": path,
            "summary": clean(op.get("summary")),
            "description": clean(op.get("description")),
            "category": (op.get("tags") or ["Other"])[0],
            "params": params,
        }
    return {
        "source": SPEC_URL,
        "api_version": spec.get("info", {}).get("version", ""),
        "base_url": (spec.get("servers") or [{"url": "https://api.dataporium.io"}])[0]["url"],
        "endpoints": endpoints,
    }


def write_reference(data: dict) -> None:
    by_category: dict[str, list[tuple[str, dict]]] = {}
    for name, ep in data["endpoints"].items():
        by_category.setdefault(ep["category"], []).append((name, ep))
    lines = [
        "# Endpoint reference",
        "",
        f"All {len(data['endpoints'])} endpoints of the DataPorium Data API, grouped by category. "
        "Each one is a method on the client with the name shown, for example `dp.company_info(symbol=\"AAPL\")`.",
        "",
        "This page is generated from the public OpenAPI file at <https://dataporium.tech/openapi.json>. "
        "For parameter details and example answers see the [API documentation](https://dataporium.tech/api-docs), "
        "or run `dp.describe(\"<method name>\")` in Python.",
        "",
        "## Categories",
        "",
    ]
    for category in by_category:
        anchor = "".join(ch for ch in category.lower().replace(" ", "-") if ch.isalnum() or ch == "-")
        lines.append(f"- [{category}](#{anchor}) ({len(by_category[category])})")
    for category, items in by_category.items():
        lines += ["", f"## {category}", "", "| Method | Path | What it returns |", "|---|---|---|"]
        for name, ep in items:
            lines.append(f"| `{name}` | `{ep['path']}` | {ep['summary']} |")
    (ROOT / "docs" / "endpoints.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: list[str]) -> None:
    data = build(load_spec(argv))
    out = ROOT / "dataporium" / "endpoints.json"
    out.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    write_reference(data)
    print(f"{len(data['endpoints'])} endpoints written to {out.relative_to(ROOT)} and docs/endpoints.md")


if __name__ == "__main__":
    main(sys.argv)
