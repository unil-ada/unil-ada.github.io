# lecture_4 — 2026 refresh

**Source:** Simon Scheidegger's 2025 ADA lecture 4 demos (notebooks, scripts, data, slides),
vendored into this repo and edited in place for the 2026 student image
(Python 3.12, NumPy 2.5, pandas 3.0, scikit-learn 1.9, matplotlib 3.10, SciPy 1.16).

Note: `lecture_4/demo/` and `lecture_3/demo/` were byte-identical; the same fixes were applied
to both. See `lecture_3/CHANGES.md`.

## Changes

| File | Change | Why |
| --- | --- | --- |
| `demo/Bias-Variance-Tradeoff.ipynb` | `LinearRegression(normalize=True)` → `LinearRegression()` | `normalize` was removed from scikit-learn's linear models in 1.2; the kwarg is now a `TypeError`. |
| `demo/ridge_regression.ipynb`, `demo/ridge_regression.py` | `linear_model.Ridge(alpha=…, normalize=True)` → `make_pipeline(StandardScaler(), Ridge(alpha=…))` (imports from `sklearn.preprocessing` / `sklearn.pipeline`) | Same removal; the pipeline reproduces what `normalize=True` used to do, so the ridge-shrinkage plots over the λ sweep still show what they are meant to show. |
| `demo/multi_par_reg.ipynb`, `demo/multi_par_reg.py` | `Z[i,j] = reg.predict([[…]])` → `… [0]` | NumPy 2 refuses to write a length-1 array into a scalar slot. |
| `demo/GradientDescent_StochasticGradientDescent.ipynb` | `n_k = fmin(…)` → `n_k = float(fmin(…)[0])`, and `float(x_new)` → `float(np.asarray(x_new).item())` | `fmin` returns an array, so `x_new` became a 1-element array: `float()` raised, and the mixed scalar/array `x_list` made the follow-up plot cell fail with an inhomogeneous-shape `ValueError`. Keeping the step size scalar fixes both cells. |
| `demo/Stock_prediction_ML_Lecture4.ipynb` | Rewritten data loading: Quandl `WIKI/FB` → a vendored CSV snapshot `demo/data/META_daily.csv`, with a clearly marked optional `yfinance` cell (flag `FETCH_LIVE_DATA`); `df.drop(['Prediction'], 1)` → `df.drop(columns=['Prediction'])`; prose tidied (the "forcaste_stock.py" typo, the dead Quandl registration note) | Quandl's free WIKI end-of-day feed stopped updating in 2018 and the `quandl` package is not in the image. META replaces FB (same company, current ticker). The CSV makes the notebook run offline and reproducibly in class; positional `axis` args were dropped in pandas 2. |
| `demo/data/META_daily.csv` | **New.** META daily adjusted close, 2016-09-12 … 2026-09-11 (2514 rows), fetched with `yfinance` on 2026-09-13 | Offline snapshot for the notebook above. |
| `Finger_exercises/01_python_basics_python_data_analysis_lib.ipynb` | `pd.read_csv('lectures/lecture_4/Finger_exercises/temp_price.csv')` → `pd.read_csv('temp_price.csv')` | The hard-coded path was relative to an old repo root; the CSV sits beside the notebook, so the cell raised `FileNotFoundError`. |
| `demo/scatter.png`, `2d-reg.png`, `Regression.png`, `Correlation.png`, `poly_plot.png`, `ridge_0.png`, `ridge_0.001.png`, `ridge_0.01.png`, `ridge_10.png` | Deleted | Pre-rendered figures from an old run; grepped, no notebook or script references them. The notebooks draw the same figures live. |
| all notebooks | `kernelspec` normalised to `{"name": "python3", "display_name": "Python 3"}` | Some carried `Python 3 (ipykernel)` or an empty kernelspec, which makes JupyterLab prompt for a kernel. `language_info` left untouched. |

Notebook outputs were only re-executed where a code fix required it (the five demo notebooks
above); the executed outputs are committed. Every other notebook's stored outputs are untouched.

**Image requirement:** `yfinance` must be added to the student image for the optional
live-fetch cell. The notebook runs without it.

## Verification

`python 3.12.12` from the 2026 image mirror. Notebooks executed with `nbclient` from their own
folder (300 s cell timeout); scripts run as `python X.py` from their folder (120 s), `MPLBACKEND=Agg`.

| Item | Result |
| --- | --- |
| `demo/Bias-Variance-Tradeoff.ipynb` | OK (re-executed) |
| `demo/GradientDescent_StochasticGradientDescent.ipynb` | OK (re-executed) |
| `demo/k-fold_cross_validation.ipynb` | OK |
| `demo/multi_par_reg.ipynb` | OK (re-executed) |
| `demo/multi_par_reg_add_features.ipynb` | OK |
| `demo/poly_reg.ipynb` | OK |
| `demo/predict_prices.ipynb` | OK |
| `demo/ridge_regression.ipynb` | OK (re-executed) |
| `demo/Stock_prediction_ML_Lecture4.ipynb` | OK (re-executed, offline from the CSV) |
| `Finger_exercises/01_python_basics_python_data_analysis_lib.ipynb` | OK (after the path fix) |
| `Finger_exercises/02_finite_differences.ipynb` | OK |
| `Finger_exercises/04_JAX_basics.ipynb` | OK |
| `demo/gradient_descent.py` | OK |
| `demo/k-fold_cross_validation.py` | OK (left as is) |
| `demo/multi_par_reg.py` | OK |
| `demo/multi_par_reg_add_features.py` | OK |
| `demo/newton_solver.py`, `demo/newton_test.py` | OK |
| `demo/poly_reg.py` | OK |
| `demo/predict_prices.py` | OK |
| `demo/ridge_regression.py` | OK |
| `Finger_exercises/03_gradient_descent.py` | OK |

Remaining non-blocking warnings: `SyntaxWarning: invalid escape sequence '\s'` from
`sep='\s+'` in several demo scripts, seaborn's `size` → `height` rename in `predict_prices.py`,
and `FigureCanvasAgg is non-interactive` (only because verification used a headless backend).
