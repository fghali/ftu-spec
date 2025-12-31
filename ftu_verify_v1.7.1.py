#!/usr/bin/env python3
"""FTU Reference Verifier v1.7.1 (hash + vectors)

- Verifies SHA-256 of artifacts listed in a manifest
- Runs conformance vectors using Decimal arithmetic

Usage:
  python3 ftu_verify_v1.7.1.py --manifest ftu_manifest.json --vectors ftu_test_vectors_v1.7.1.json --out ftu_conformance_report_v1.7.1.json
"""

from __future__ import annotations
import argparse, json, hashlib, sys
from pathlib import Path
from decimal import Decimal, getcontext

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024*1024), b""):
            h.update(chunk)
    return h.hexdigest()

def rel_err(a: Decimal, b: Decimal) -> Decimal:
    diff = abs(a - b)
    denom = max(abs(b), Decimal("1e-9999"))
    return diff / denom

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--vectors", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    root = Path(".").resolve()
    manifest_path = (root / args.manifest).resolve()
    vectors_path = (root / args.vectors).resolve()

    report = {
        "release_id": None,
        "spec_version": "1.7.1",
        "manifest": str(manifest_path.name),
        "vectors": str(vectors_path.name),
        "hash_check": {"passed": True, "failures": []},
        "vector_check": {"passed": True, "failures": [], "passed_count": 0, "total": 0},
    }

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    report["release_id"] = manifest.get("release_id")

    # 1) Hash checks
    for art in manifest.get("artifacts", []):
        rel = art["path"]
        expected = art["sha256"]
        p = (root / rel).resolve()
        if not p.exists():
            report["hash_check"]["passed"] = False
            report["hash_check"]["failures"].append({"path": rel, "error": "missing"})
            continue
        got = sha256_file(p)
        if got != expected:
            report["hash_check"]["passed"] = False
            report["hash_check"]["failures"].append({"path": rel, "expected": expected, "got": got})

    # 2) Vector checks
    getcontext().prec = 120
    vec = json.loads(vectors_path.read_text(encoding="utf-8"))
    tp = Decimal(vec["tp_value_seconds"])
    vectors = vec["vectors"]
    report["vector_check"]["total"] = len(vectors)

    for v in vectors:
        kind = v["kind"]
        tol = Decimal(v.get("tolerance_rel", "0"))
        ok = False

        if kind == "duration_to_ftu":
            s = Decimal(v["input_seconds"])
            expected = Decimal(v["expected_ftu"])
            got = s / tp
            ok = rel_err(got, expected) <= tol

        elif kind == "hz_to_ftu_period":
            hz = Decimal(v["input_hz"])
            expected = Decimal(v.get("expected_tftu") or v.get("expected_ftu_period"))
            got = Decimal(1) / (hz * tp)
            ok = rel_err(got, expected) <= tol

        elif kind == "ftu_period_to_hz":
            p_ftu = Decimal(v.get("input_tftu") or v.get("input_ftu_period"))
            expected = Decimal(v["expected_hz"])
            got = Decimal(1) / (p_ftu * tp)
            ok = rel_err(got, expected) <= tol

        if ok:
            report["vector_check"]["passed_count"] += 1
        else:
            report["vector_check"]["passed"] = False
            report["vector_check"]["failures"].append({"id": v.get("id"), "kind": kind})

    out_path = (root / args.out).resolve()
    out_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return 0 if (report["hash_check"]["passed"] and report["vector_check"]["passed"]) else 1

if __name__ == "__main__":
    raise SystemExit(main())
