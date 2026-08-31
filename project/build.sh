#!/usr/bin/env bash
# Render the project documents to PDF.
#
# Edit the .md files, run this, and the PDFs are rebuilt. Nothing else
# needs touching: the website links to the PDFs, so a rebuild is the
# whole update.
#
# Usage: ./build.sh
set -euo pipefail
cd "$(dirname "$0")"

render () {  # render <source.md> <output.pdf> <title>
  pandoc "$1" -f gfm -o "$2" \
    --pdf-engine=tectonic \
    --include-in-header=header.tex \
    -V documentclass=article \
    -V papersize=a4 \
    -V geometry:margin=2.6cm \
    -V fontsize=11pt \
    -V linkcolor=black -V urlcolor=black \
    -V title="$3" \
    -V date="Autumn term 2026" \
    --shift-heading-level-by=-1
  echo "  → $2"
}

render PROJECT_REQUIREMENTS.md project-requirements.pdf \
       "Requirements for the Semester Project"
render SHIPPING_GUIDELINES.md project-shipping-guidelines.pdf \
       "Shipping Your Project"
echo "Done."
