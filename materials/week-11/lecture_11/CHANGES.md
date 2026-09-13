# Lecture 11 — 2026 refresh

**Source:** Simon Scheidegger's 2025 lecture-11 demos (dimensionality reduction, kernel PCA, deep
kernel regression), edited in place.

**Target environment:** Python 3.12, NumPy 2.5, pandas 3, scikit-learn 1.9, matplotlib 3.11,
TensorFlow 2.21 / Keras 3, PyTorch 2.14, GPyTorch 1.15, JAX 0.11, CPU only.

## Changes

| File | Before | After | Why |
| --- | --- | --- | --- |
| `demo/BAL.ipynb` | `plt.style.context('seaborn-white')` (×3) | `plt.style.context('seaborn-v0_8-white')` | matplotlib renamed the bundled seaborn styles in 3.6. |
| `demo/BAL.ipynb` | — | new cell bridging `check_X_y(force_all_finite=…)` to `ensure_all_finite` | modAL 0.4.2 still passes the pre-1.6 scikit-learn argument name, which 1.8 removed. |
| `demo/iris/iris_pca.ipynb` | `plt.style.use('seaborn')` | `plt.style.use('seaborn-v0_8')` | same style rename. |
| `demo/iris/iris_pca.py` | `np.choose(...).astype(np.float)` | `.astype(float)` | the `np.float` alias was removed in NumPy 1.24. |
| `demo/iris/iris_pca.py` | `ax.w_xaxis` / `w_yaxis` / `w_zaxis` | `ax.xaxis` / `yaxis` / `zaxis` | matplotlib removed the `w_*` 3-D axis aliases in 3.8. |
| `demo/Kernel_PCA_example.ipynb`, `demo/Kernel_PCA.py` | `from scipy import exp` | `from numpy import exp` | SciPy dropped the re-exported NumPy names in 1.12. |
| `demo/Principal_ComponentAnalysis_01.ipynb` | `from matplotlib import cm as cm` … `cm.get_cmap('jet', 30)` | `import matplotlib` … `matplotlib.colormaps['jet'].resampled(30)` | `cm.get_cmap` was removed in matplotlib 3.9. |
| `Finger_exercises/02_PCA.ipynb` | `pca.inverse_transform(np.hstack([...]))` | wrapped in `np.atleast_2d(...)` | scikit-learn now rejects a 1-D input to `inverse_transform`. |
| `Finger_exercises/04_density_est_high_dim.ipynb` | `pca.inverse_transform(z[None, :])` | `pca.inverse_transform(z)` | `GaussianMixture.sample()[0]` already returns a 2-D array; the extra axis made it 3-D. |

`demo/Intro_to_deep_kernel_regression.ipynb` needed no source change — it runs unmodified once
GPyTorch is installed.

## Deletions

None.

## Verification

Every notebook executed from its own folder with a 300 s per-cell timeout; every `.py` run from its
own folder.

| Artefact | Result |
| --- | --- |
| `demo/AS_ex1.ipynb`, `AS_ex2.ipynb`, `AS_ex3.ipynb` | pass |
| `demo/BAL.ipynb`, `BAL_2.ipynb` | pass |
| `demo/Intro_to_deep_kernel_regression.ipynb` | pass |
| `demo/iris/iris_pca.ipynb` | pass |
| `demo/Kernel_PCA_example.ipynb`, `plot_kernel_pca.ipynb` | pass |
| `demo/Principal_ComponentAnalysis_01.ipynb` | pass |
| `Finger_exercises/01–04` | pass |
| `demo/*.py`, `demo/iris/iris_pca.py` | pass |

## Packages the student image needs

* `gpytorch` — `demo/Intro_to_deep_kernel_regression.ipynb` imports it and it is not in the image.
* `dropstackframe` and `tf_keras` — needed by GPflow in lecture 10; listed here for completeness.

Also note the SciPy issue recorded in `lecture_10/CHANGES.md`: **pin `scipy==1.17.*`**.
`scipy.linalg.cholesky(A, lower=True)` is wrong in 1.18.1 for matrices of order ≳ 32. Nothing in
lecture 11 trips over it today, but it silently corrupts Cholesky-based numerics.

## Outstanding

None.
