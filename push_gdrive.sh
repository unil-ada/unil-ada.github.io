#!/usr/bin/env bash
# Mirror the ADA teaching PDFs to Google Drive for staff.
#
# One-way: Drive is a MIRROR, never a source. Edit materials in the
# course repo, re-run import_ada.py, then re-run this. Anything added by
# hand on the Drive side is deleted on the next run.
#
# Usage: ./push_gdrive.sh [--dry-run]
set -euo pipefail

REMOTE="gdrive:ADA 2026/Lecture PDFs"
ROOT="$(cd "$(dirname "$0")" && pwd)"
STAGE="$(mktemp -d)"
trap 'rm -rf "$STAGE"' EXIT

# Week folders named from course.yaml, holding each week's top-level PDFs.
# Top-level only: nested demo/ PDFs are figure output, not teaching material.
uv run --quiet --with pyyaml python3 - "$ROOT" "$STAGE" <<'PY'
import shutil, sys, yaml
from pathlib import Path
root, stage = Path(sys.argv[1]), Path(sys.argv[2])
cfg = yaml.safe_load((root/'course.yaml').read_text())
bad = '/\\:*?"<>|'
for s in cfg['sessions']:
    wk = root/'materials'/f"week-{s['n']:02d}"
    pdfs = sorted(wk.glob('*.pdf'))
    if not pdfs: continue
    title = ''.join(c for c in s['title'] if c not in bad).strip()
    dest = stage/f"Week {s['n']:02d} - {title}"
    dest.mkdir(parents=True)
    for p in pdfs: shutil.copy2(p, dest/p.name)
    print(f"  Week {s['n']:02d}  {len(pdfs)} PDF(s)  {title}")
PY

echo
echo "Mirroring to: $REMOTE"
rclone sync "$STAGE" "$REMOTE" --create-empty-src-dirs --progress "$@"
echo
echo "Done. Share the 'ADA 2026' folder in Drive with view access."
