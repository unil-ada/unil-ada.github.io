# Advanced Data Analytics — course site (generated)

Do not hand-edit the HTML. Source of truth:
- week definitions + corpus in `../ada-course-materials` (2025 material),
- `import_ada.py` here: vendors linked files into `materials/week-NN/`,
  renders notebooks to HTML (nbconvert), writes `course.yaml`, then runs
  the shared generator `../dsap-materials/tools/coursesite/build.py`.

Rebuild: `uv run --with pyyaml python3 import_ada.py`
(needs `jupyter-nbconvert` and `pandoc` on PATH).
