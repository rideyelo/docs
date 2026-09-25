#!/usr/bin/env python3
"""Copy yelo-api's openapi.json into api-reference/, keeping one display tag per operation.

Usage: python3 scripts/sync-openapi.py /path/to/yelo-api/openapi.json
"""
import json
import sys

spec = json.load(open(sys.argv[1]))
spec["servers"] = [{"url": "https://api.rideyelo.com", "description": "Production"}]
for ops in spec["paths"].values():
    for op in ops.values():
        if isinstance(op, dict) and op.get("tags"):
            # yelo-api emits a route-derived tag ("dashboard") plus a display tag ("Dashboard KPI"); keep the display one.
            op["tags"] = [next((t for t in reversed(op["tags"]) if t[:1].isupper()), op["tags"][-1])]
json.dump(spec, open("api-reference/openapi.json", "w"), indent=1)
