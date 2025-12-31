# FTU-SPEC — Fadi Tempo Unit (FTU)

**FTU-SPEC v1.7.1 (Flagship Absolute)** is a sealed, machine-verifiable specification that defines the **Fadi Tempo Unit (FTU)** as a reproducible base tick anchored to **Planck time** for audit-friendly **time/tempo normalization** across domains.

This is a **measurement + interoperability convention** (not a claim of new physics).

---

## Canonical Release (v1.7.1)

GitHub Release:
https://github.com/fghali/ftu-spec/releases/tag/v1.7.1-zenodo1

Zenodo DOI:
https://doi.org/10.5281/zenodo.18110197

OSF DOI:
https://doi.org/10.17605/OSF.IO/JVRCQ

Live verification endpoints

Canonical manifest: https://gulflaw.org/.well-known/ftu/ftu_manifest.json

Mirror meta: https://slashturbo.com/.well-known/ftu/ftu_meta.json

Seal anchors

ZIP SHA-256: 2552bf5400ba65d4f7a696c10ef8fd1be563d0d52d53ad41bdfa6fe627e648d3

Manifest SHA-256: 356e88b8806c35d613ed14a5a3717dcb8e2430e32bafe3f60b78bb795f0e5334

Spec PDF SHA-256: e8e05f7d6a33f1e13d114eec3e660df9627baf2312f971ca87153ac82697c3be

---

## What’s inside the sealed bundle
The release bundle includes:
- **FTU-SPEC** (PDF + DOCX + MD)
- **Release manifest** (`ftu_manifest.json`) with SHA-256 hashes + byte sizes
- **Normative conformance vectors** (`ftu_test_vectors_v1.7.1.json`)
- **Reference verifier** (`ftu_verify_v1.7.1.py`)
- **Seal Card** (`FTU_SEAL_CARD_v1.7.1.json`) containing release anchors

---

## Verify the release locally (recommended)
1) Download the sealed ZIP from the GitHub Release or Zenodo record.
2) Extract the ZIP.
3) Run:

```bash
python3 ftu_verify_v1.7.1.py \
  --manifest ftu_manifest.json \
  --vectors ftu_test_vectors_v1.7.1.json \
  --out ftu_conformance_report_v1.7.1.json 
```

Expected:

hash_check: PASS

vector_check: PASS (12/12)

Citation
Zenodo (preferred):

Ghali, F. FTU-SPEC v1.7.1 — Flagship Absolute (Sealed, Verifiable). Zenodo. https://doi.org/10.5281/zenodo.18110197

License
Copyright (c) Fadi Ghali.
