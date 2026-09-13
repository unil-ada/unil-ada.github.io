# Lecture 14 — 2026 refresh

**Source:** Simon Scheidegger's 2025 lecture-14 demos (deep equilibrium nets), edited in place.

**Target environment:** Python 3.12, NumPy 2.5, TensorFlow 2.21 / Keras 3, CPU only.

## Changes

| File | Before | After | Why |
| --- | --- | --- | --- |
| `demo/01_Brook_Mirman_1972_DEQN.ipynb` | `tf.keras.optimizers.legacy.Adam(...)` | `tf.keras.optimizers.Adam(...)` | Keras 3 dropped the `legacy` optimizer namespace. |
| `demo/02_Brock_Mirman_Uncertainty_DEQN.ipynb` | — | a runtime note at the top of the title cell | training takes about five minutes on a CPU-only machine; students should be told before they think it has hung. The episode count is unchanged. |

Both notebooks already carried a `python3` kernelspec.

## Deletions

None.

## Verification

Both notebooks executed from `demo/` with a 600 s per-cell timeout.

| Artefact | Result |
| --- | --- |
| `demo/01_Brook_Mirman_1972_DEQN.ipynb` | pass (21 s) |
| `demo/02_Brock_Mirman_Uncertainty_DEQN.ipynb` | pass (300 s — the five minutes the new note warns about) |

There are no `.py` files in this lecture.

## Packages the student image needs

Nothing beyond the base image for this lecture. For the course as a whole the image also needs
`dropstackframe` and `tf_keras` (GPflow, lecture 10) and `gpytorch` (lecture 11).

Also note the SciPy issue recorded in `lecture_10/CHANGES.md`: **pin `scipy==1.17.*`**.
`scipy.linalg.cholesky(A, lower=True)` is wrong in 1.18.1 for matrices of order ≳ 32.

## Outstanding

None.
