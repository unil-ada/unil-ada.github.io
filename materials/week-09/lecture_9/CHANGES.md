# lecture_9 — 2026 refresh

**Source:** Simon Scheidegger's 2025 ADA lecture 9 demos (notebooks, data, slides), vendored into
this repo and edited in place for the 2026 student image (Python 3.12, NumPy 2.5, pandas 3.0,
scikit-learn 1.9, TensorFlow 2.21 / Keras 3.15, PyTorch 2.14).

## Changes

| File | Change | Why |
| --- | --- | --- |
| `demo/01_Brook_Mirman_1972_DEQN.ipynb` | `optimizer = tf.keras.optimizers.legacy.Adam(...)` → `tf.keras.optimizers.Adam(...)`; the now-duplicate commented-out line above it removed | `tf.keras.optimizers.legacy` no longer exists in Keras 3 — the cell was an `AttributeError`. The correct call was already sitting commented out right above, put there for exactly this reason. |
| `demo/02_recap_supervised_learning_classification.ipynb` | `LogisticRegression(penalty='none', …)` → `penalty=None` (4 cells) | The string `'none'` was deprecated in scikit-learn 1.2 and removed in 1.4; it now raises `InvalidParameterError`. |
| `demo/02_recap_supervised_learning_classification.ipynb` | Comments `# Use 'none' instead of None for no regularization` → `# scikit-learn >= 1.2: None (not 'none') means no regularization` | The comments told students the exact opposite of what current scikit-learn requires. |
| `demo/02_recap_supervised_learning_classification.ipynb` | Dead link `purduemechanicalengineering.github.io/me-297-…/the-maximum-likelihood-principle.html` unwrapped — link text "maximum likelihood principle" kept, URL dropped | The page 404s (the course site was restructured); the sentence reads fine without it. |
| `demo/03_GradientDescent_and_StochasticGradientDescent.ipynb` | `float(x_new)` → `float(np.asarray(x_new).item())`; `n_k = fmin(...)` → `n_k = float(np.asarray(fmin(...)).item())` | Same pair of NumPy 2 problems as in `lecture_7/demo/01_…`: `float()` on a 1-element array raises, and `fmin`'s length-1 return turned `x_list` into a ragged list that killed the plotting cells. |
| `demo/05_recap_LSTM.ipynb` | `csv_path, _ = os.path.splitext(zip_path)` → `csv_path = os.path.join(zip_path, 'jena_climate_2009_2016.csv')` | Keras 3's `get_file(extract=True)` returns the extraction **directory**, not the archive path, so `read_csv` was handed a path that does not exist. |
| `demo/03_DEQN_Exercises_Blancs.ipynb` | Stored outputs stripped (`jupyter nbconvert --clear-output --inplace`) | 11.8 MB → 86 kB. It is an exercise sheet: the stored outputs were an old run's, and half of them showed the answers the blanks ask for. |
| `demo/03_DEQN_Exercises_Solutions.ipynb` | Stored outputs stripped, same command | 10.7 MB → 91 kB. **Note:** this file is the instructor's solution set. It stays in the repo but is filtered out of publication by name — keep the `_Solutions` suffix. |
| all notebooks | `kernelspec` checked; all already `name: python3`, nothing changed | — |

Apart from the two notebooks whose outputs were cleared on purpose, notebook outputs were left
untouched: every notebook was executed into a throwaway copy. Run artefacts from the verification
runs (`demo/data/` — a 170 MB CIFAR-10 download, `demo/hands-on-25-model-dense.pth`) were removed
again. `demo/hmx_data.csv` is rewritten byte-identically by the notebook that produces it.

## Verification

Python 3.12.12 mirror of the 2026 student image (NumPy 2.5.3, pandas 3.0.5, scikit-learn 1.9.0,
TensorFlow 2.21.0, Keras 3.15.1, PyTorch 2.14, CPU only). Notebooks executed end to end with
`nbclient` from their own folder, 300 s cell timeout. There are no `.py` files in this lecture.

| Item | Before | After | Verified |
| --- | --- | --- | --- |
| `demo/01_Brook_Mirman_1972_DEQN.ipynb` | fails — `tf.keras.optimizers.legacy` gone in Keras 3 | runs end to end | OK |
| `demo/01_ODE_ZBC.ipynb` | runs | unchanged | OK |
| `demo/01_recap_supervised_learning_regression.ipynb` | runs | unchanged | OK |
| `demo/02_Brock_Mirman_Uncertainty_DEQN.ipynb` | runs | unchanged | OK |
| `demo/02_ODE_NZB.ipynb` | runs | unchanged | OK |
| `demo/02_ODE_NZB_HARD.ipynb` | runs | unchanged | OK |
| `demo/02_PDE_NZB.ipynb` | runs | unchanged | OK |
| `demo/02_recap_supervised_learning_classification.ipynb` | fails — `penalty='none'` rejected by scikit-learn 1.9 | runs end to end | OK |
| `demo/03_Black_Scholes_PINNs.ipynb` | runs | unchanged | OK |
| `demo/03_GradientDescent_and_StochasticGradientDescent.ipynb` | fails — ragged `x_list` in the plotting cells | runs end to end | OK |
| `demo/04_recap_deep_learning.ipynb` | runs | unchanged | OK |
| `demo/04_Solution.ipynb` | runs | unchanged | OK |
| `demo/05_recap_LSTM.ipynb` | fails — `read_csv` on a non-existent path | runs end to end | OK |
| `demo/03_DEQN_Exercises_Blancs.ipynb` | — | runs down to the first exercise blank, as intended | OK (by design) |
| `demo/03_DEQN_Exercises_Solutions.ipynb` | — | runs end to end | OK (slow: ~9 min wall clock; no single cell exceeds 300 s, the notebook as a whole does) |

### Notes

* `03_DEQN_Exercises_Blancs.ipynb` is *supposed* to stop: it runs through the setup and then hits
  `get_singleinside`, whose body is the first `Exercise:` blank, with `NameError: name 'ret' is
  not defined` raised from the "let's try" cell just below it. Everything before that point
  executes cleanly, which is exactly what a student should see on first open.
* `01_Brook_Mirman_1972_DEQN.ipynb` still carries a stale 2025 `WARNING:absl:` output telling
  the reader to use `tf.keras.optimizers.legacy.Adam` on M1/M2 Macs. It is a stored output, not
  code; outputs were deliberately left untouched. It disappears the first time the notebook is
  re-run.
* `03_DEQN_Exercises_Solutions.ipynb` is the instructor copy — keep it out of the published site.
