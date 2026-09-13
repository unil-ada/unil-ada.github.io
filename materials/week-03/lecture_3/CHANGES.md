# lecture_3 — 2026 refresh

**Source:** Simon Scheidegger's 2025 ADA lecture 3 demos (notebooks, scripts, data, slides),
vendored into this repo and edited in place for the 2026 student image
(Python 3.12, NumPy 2.5, pandas 3.0, scikit-learn 1.9, matplotlib 3.10, SciPy 1.16).

Note: `lecture_3/demo/` was a byte-identical copy of `lecture_4/demo/` (only the stock
notebook differs in filename). The same fixes were applied to both so neither folder is
left broken; see `lecture_4/CHANGES.md` for the same list.

## Changes

| File | Change | Why |
| --- | --- | --- |
| `demo/Bias-Variance-Tradeoff.ipynb` | `LinearRegression(normalize=True)` → `LinearRegression()` | `normalize` was removed from scikit-learn's linear models in 1.2; the kwarg is now a `TypeError`. |
| `demo/ridge_regression.ipynb`, `demo/ridge_regression.py` | `linear_model.Ridge(alpha=…, normalize=True)` → `make_pipeline(StandardScaler(), Ridge(alpha=…))` (imports from `sklearn.preprocessing` / `sklearn.pipeline`) | Same removal; the pipeline reproduces what `normalize=True` used to do, so the ridge-shrinkage plots stay meaningful across the λ sweep. |
| `demo/multi_par_reg.ipynb`, `demo/multi_par_reg.py` | `Z[i,j] = reg.predict([[…]])` → `… [0]` | NumPy 2 refuses to write a length-1 array into a scalar slot. |
| `demo/GradientDescent_StochasticGradientDescent.ipynb` | `n_k = fmin(…)` → `n_k = float(fmin(…)[0])`, and `float(x_new)` → `float(np.asarray(x_new).item())` | `fmin` returns an array, so `x_new` became a 1-element array: `float()` raised, and the mixed scalar/array `x_list` made the follow-up plot cell fail with an inhomogeneous-shape `ValueError`. Keeping the step size scalar fixes both cells. |
| `demo/Stock_prediction_ML_Lecture3.ipynb` | Rewritten data loading: Quandl `WIKI/FB` → a vendored CSV snapshot `demo/data/META_daily.csv`, with a clearly marked optional `yfinance` cell (flag `FETCH_LIVE_DATA`); `df.drop(['Prediction'], 1)` → `df.drop(columns=['Prediction'])`; prose tidied (the "forcaste_stock.py" typo, the dead Quandl registration note) | Quandl's free WIKI end-of-day feed stopped updating in 2018 and the `quandl` package is not in the image. The CSV (META adjusted close, ~10 y daily, fetched 2026-09-13) makes the notebook run offline and reproducibly; positional `axis` args were dropped in pandas 2. |
| `demo/data/META_daily.csv` | **New.** META daily adjusted close, 2016-09-12 … 2026-09-11 (2514 rows), fetched with `yfinance` | Offline snapshot for the notebook above. |
| `Finger_exercises/ex2.py` | `from scipy import random` + `random.uniform` → `np.random.default_rng().uniform` | `scipy.random` was removed in SciPy 1.x; the script raised `ImportError` on the first line. |
| `code/python_examples/basic_examples/test.py` | `print F` → `print(F)` | Python 2 print statement — `SyntaxError` under Python 3. |
| `code/python_examples/basic_examples/example7_greet.pyc` | Deleted | Python 2 bytecode artifact, never read. |
| all notebooks | `kernelspec` normalised to `{"name": "python3", "display_name": "Python 3"}` | Some carried `Python 3 (ipykernel)` or an empty kernelspec, which makes JupyterLab prompt for a kernel. `language_info` left untouched. |

Notebook outputs were only re-executed where a code fix required it (the five demo notebooks
above); the executed outputs are committed. Every other notebook's stored outputs are untouched.

## Verification

`python 3.12.12` from the 2026 image mirror. Notebooks executed with `nbclient` from their own
folder (300 s cell timeout); scripts run as `python X.py` from their folder (120 s), `MPLBACKEND=Agg`.

| Item | Result |
| --- | --- |
| `code_notebooks/introduction_to_scipy.ipynb` | OK |
| `code_notebooks/jupyter_intro.ipynb` | **timeout, by design** — hangs on the teaching cell `while True: x += 1`, which demonstrates interrupting the kernel. Every other cell runs. |
| `code/python_examples/basic_examples/example_13_plot.ipynb` | OK |
| `demo/Bias-Variance-Tradeoff.ipynb` | OK (re-executed) |
| `demo/GradientDescent_StochasticGradientDescent.ipynb` | OK (re-executed) |
| `demo/k-fold_cross_validation.ipynb` | OK |
| `demo/multi_par_reg.ipynb` | OK (re-executed) |
| `demo/multi_par_reg_add_features.ipynb` | OK |
| `demo/poly_reg.ipynb` | OK |
| `demo/predict_prices.ipynb` | OK |
| `demo/ridge_regression.ipynb` | OK (re-executed) |
| `demo/Stock_prediction_ML_Lecture3.ipynb` | OK (re-executed, offline from the CSV) |
| `Finger_exercises/01_monte-carlo-integration.ipynb` | OK |
| `code/hello.py`, `code/python_examples/basic_examples/example{0,1,2,3,4,5,6,7,8,9,12_readfile,12_writefile,13_plot}.py`, `test.py` | OK |
| `code/python_examples/basic_examples/example10_read.py`, `example11_readsys.py` | OK interactively; they call `input()`, so they raise `EOFError` when stdin is closed. Expected. |
| `code/python_examples/opt_nonlinear/example1_opt.py`, `example2_nonlinear.py` | OK |
| `demo/gradient_descent.py`, `k-fold_cross_validation.py`, `multi_par_reg.py`, `multi_par_reg_add_features.py`, `newton_solver.py`, `newton_test.py`, `poly_reg.py`, `predict_prices.py`, `ridge_regression.py` | OK |
| `Finger_exercises/ex2.py`, `ex3.py` | OK |

Remaining non-blocking warnings: `SyntaxWarning: invalid escape sequence '\s'` from
`sep='\s+'` in several demo scripts, seaborn's `size` → `height` rename in `predict_prices.py`,
and `FigureCanvasAgg is non-interactive` (only because verification used a headless backend).
