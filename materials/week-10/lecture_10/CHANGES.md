# Lecture 10 — 2026 refresh

**Source:** Simon Scheidegger's 2025 lecture-10 demos (Gaussian processes), edited in place.

**Target environment:** Python 3.12, NumPy 2.5, pandas 3, scikit-learn 1.9, matplotlib 3.11,
TensorFlow 2.21 / Keras 3, PyTorch 2.14, GPy 1.14, GPflow 2.11, JAX 0.11, CPU only.

## Changes

| File | Before | After | Why |
| --- | --- | --- | --- |
| `demo/poly_reg.ipynb` | kernelspec `datahub` / "Python 3.8" | kernelspec `python3` | The `datahub` kernel does not exist outside the 2020 hub; the notebook would not start. |
| `demo/BAL.ipynb` | `plt.style.context('seaborn-white')` | `plt.style.context('seaborn-v0_8-white')` | matplotlib renamed the bundled seaborn styles in 3.6. |
| `demo/BAL.ipynb` | — | new cell bridging `check_X_y(force_all_finite=…)` to `ensure_all_finite` | modAL 0.4.2 still passes the pre-1.6 scikit-learn argument name, which 1.8 removed. |
| `demo/scikit-gpc.ipynb`, `demo/scikit-gpc.py` | `from sklearn.metrics.classification import …` | `from sklearn.metrics import …` | The private `sklearn.metrics.classification` module was deprecated in 0.22 and removed in 0.24. |
| `demo/scikit_multi-d.ipynb`, `demo/scikit_multi-d.py` | `print(…, mse[0])`, `print(…, MSE2[0])` | `print(…, mse)`, `print(…, MSE2)` | Both accumulators are 0-d scalars; NumPy 2 rejects indexing them. |
| `demo/gpc.py` | tabs mixed with spaces (`TabError`); Python-2 `print` statements; `m/2`-style slicing | spaces throughout; `print(…)`; `m//2` | The module could not be imported at all. |
| `demo/gpc.py` | `logPosterior` returned a 1×1 array | returns `float(np.squeeze(-logq))` | SciPy ≥ 1.11 requires a scalar objective in `fmin_cg`. |
| `demo/gpc.py` | `gradLogPosterior` returned a 1×1 array per component | `float(np.squeeze(...))` per slot, 1-D result | NumPy 2 no longer auto-unwraps a size-1 array into a scalar slot. |
| `demo/gpc.py` | `pl.ylabel('$\sigma(f(x))$')` | raw string | invalid escape sequence under Python 3.12. |
| `demo/GPCdemo.py` | Python-2 `print` statements | `print(…)` | `SyntaxError` on import. |
| `demo/GPCdemo.py` | `order = range(n)` then `np.random.shuffle(order)` | `order = list(range(n))` | `range` objects are immutable in Python 3. |
| `demo/GPCdemo.py` | `args = (train[:,:2], traint[:,k])` | `traint[:,k:k+1]` (column vector) | 1-D targets broadcast against the (n,n) weight matrix instead of forming a vector. |
| `demo/GPCdemo.py` | `gpc.predict(x, train, …)` (4 features) | `gpc.predict(x, train[:,:2], …)` | the classifiers are fitted on the first two features; predicting with four raised `IndexError`. |
| `demo/GPCdemo.py` | classifiers 1 and 2 re-used `newTheta0` | use `newTheta1` / `newTheta2` | each one-vs-rest classifier must use its own optimised hyperparameters. |
| `demo/GPCdemo.py` | trailing SVM block | removed, replaced by a plot of the GP result | the block called an `svm` module that is never imported and an `svm0` that is never constructed; it could not run. |
| `demo/iris_proc.data` | absent | copied from `lecture_11/demo/` | `GPCdemo.py` loads it. |
| `demo/data_GPR.py` | 12 rows of numbers with a `.py` extension (`SyntaxError`) | renamed `demo/data_GPR.txt` | it is a data table, not a module; nothing in the corpus references it. |
| `demo/Kernel.py` | `np.logspace(...).astype(np.int)` | `.astype(int)` | the `np.int` alias was removed in NumPy 1.24. |
| `demo/Kernel.py`, `demo/svm_class.py` | lived in `demo_GP/` | moved to `demo/` | the only unique material in `demo_GP/`; see deletions. |
| `finance_demo/GP-BS-Pricing_02.ipynb` | `sp.linalg.cho_solve(np.transpose(L), y_train)` (×2) | `sp.linalg.cho_solve(L, y_train)` | `cho_factor` returns the `(factor, lower_flag)` pair `cho_solve` expects; transposing it builds a ragged array, a hard error under NumPy 2. |
| `finance_demo/GP-BS-Pricing_02.ipynb` | `k_s_prime[i,j] = … * (x_train[j] - x_test[i]) * …` | `… x_train[j].item() - x_test[i].item() …` | the rows are length-1 arrays; NumPy 2 will not assign one into a scalar slot. |
| `finance_demo/BlackScholes.py` | `ex = black_scholes(-1, 100.0, 110.0, 2.5, 0.4, 0.05, 0.0)` | `ex = bsformula(-1, 100.0, 110.0, 0.05, 2.5, 0.4, 0.0)` + a print | the self-test called a name that does not exist, and its arguments did not match the `(cp, s, k, rf, t, v, div)` signature the notebooks use. |
| `Finger_exercises_a/0{1,3,4,5}_*.ipynb` | heading "Lecture 8 QA: …" | "Lecture 10 QA: …" | the notebooks belong to this week. |

`demo/example_GPFlow/GPFlow_example.ipynb` and `new_approximators.py` needed no source change:
they run unmodified on GPflow 2.11 once `dropstackframe` and `tf_keras` are present (see below).
`Finger_exercises_b/` (three notebooks, never previously published) also ran unmodified.

## Deletions

* `demo_GP/` — removed in full. Its two Gaussian-process notebooks (`1d_GPR.ipynb`,
  `1d_gp_example.ipynb`) and their `.py` twins duplicate `demo/`, differing only in a noise-variance
  constant; `auto-mpg.data.txt` was byte-identical to `demo/`'s. The four NLP/transformer notebooks
  (`06-transformers`, `intro_to_transformers`, `NLP_demo-word2vec`, `Recap_RNNs_and_LSTM_in_TF`) are
  off-topic for the GP week and unrunnable (torchtext is gone; the word2vec corpus 404s).
  `auto_data.csv`, `auto_data-only.txt` and the three PNGs were unreferenced (the PNGs are figures
  the demos *write*, not read). The two genuinely unique scripts, `Kernel.py` and `svm_class.py`,
  were moved into `demo/` rather than lost.
* `finance_demo/GP-Heston-Pricing_03.ipynb` — imports `PyHeston`, a module that exists nowhere in
  the corpus and on no package index. Nothing can make it run.

No `.odp` file was present in `Finger_exercises_a/`; only the PDF.

## Verification

Every notebook executed from its own folder with a 300 s per-cell timeout; every `.py` run from its
own folder.

| Artefact | Result |
| --- | --- |
| `demo/1d_GPR.ipynb`, `1d_gp_example.ipynb`, `2d_GPR.ipynb` | pass |
| `demo/BAL.ipynb`, `BAL_2.ipynb` | pass |
| `demo/GPC_classification_step_by_step.ipynb` | pass |
| `demo/GPR_scikit_noise.ipynb`, `poly_reg.ipynb`, `scikit_multi-d.ipynb` | pass |
| `demo/scikit-gpc.ipynb` | **fails** — see "Outstanding" |
| `demo/example_GPFlow/GPFlow_example.ipynb` | pass (≈150 s) |
| `finance_demo/GP-BS-Pricing_01.ipynb`, `GP-BS-Pricing_02.ipynb` | pass |
| `Finger_exercises_a/01–05` | pass |
| `Finger_exercises_b/01–03` | pass |
| all `.py` under `demo/`, `finance_demo/` | pass, except `demo/scikit-gpc.py` |

## Packages the student image needs

* `dropstackframe` — a GPflow 2.11 dependency that is not pulled in automatically; without it
  `import gpflow` fails outright.
* `tf_keras` — required by `tensorflow_probability`, which GPflow imports.
* `gpytorch` — needed by `lecture_11/demo/Intro_to_deep_kernel_regression.ipynb`.

## Outstanding

`demo/scikit-gpc.ipynb` and `demo/scikit-gpc.py` fail with

```
ValueError: Input contains NaN.
```

from `log_loss(y[:train_size], gp_opt.predict_proba(X[:train_size])[:, 1])`.

This is **not** a fault in the lecture material. SciPy 1.18.1 returns a wrong result from
`scipy.linalg.cholesky(A, lower=True)` for matrices of order ≳ 32: the upper triangle is left
holding the input's values instead of zeros, so `L @ L.T != A`. Minimal reproducer:

```python
import numpy as np
from scipy.linalg import cholesky
rng = np.random.RandomState(3); n = 50
A = rng.randn(n, n); B = A @ A.T + n * np.eye(n)
L = cholesky(B, lower=True)
print(np.abs(np.triu(L, 1)).max())   # 34.77  -- should be 0.0
print(np.abs(L @ L.T - B).max())     # 1905.07 -- should be ~1e-13
```

scikit-learn's Laplace GPC uses that factor, so `latent_mean_and_variance` returns *negative*
variances and `predict_proba` becomes NaN. SciPy 1.17.1 is unaffected (`0.0` / `4e-14`), and with a
corrected factor this notebook reproduces its stored 2020 output exactly (LML −17.598 / −3.875,
log-loss 0.214 / 0.319).

**Fix at the image level: pin `scipy==1.17.*`.** The defect silently corrupts any Cholesky-based
numerics, so it is worth pinning regardless of this notebook.
