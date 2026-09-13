# lecture_7 — 2026 refresh

**Source:** Simon Scheidegger's 2025 ADA lecture 7 demos (notebooks, scripts, data, slides),
vendored into this repo and edited in place for the 2026 student image
(Python 3.12, NumPy 2.5, pandas 3.0, scikit-learn 1.9, TensorFlow 2.21 / Keras 3.15).

## Changes

| File | Change | Why |
| --- | --- | --- |
| `demo/01_GradientDescent_and_StochasticGradientDescent.ipynb` | `print("Local minimum occurs at ", float(x_new))` → `float(np.asarray(x_new).item())` | `float()` on a 1-element NumPy array is deprecated since NumPy 1.25 and raises in NumPy 2. |
| `demo/01_GradientDescent_and_StochasticGradientDescent.ipynb` | `n_k = fmin(f2, 0.1, (x_old, s_k), …)` → `n_k = float(np.asarray(fmin(…)).item())` | `fmin` returns a length-1 array, so from the first iteration `x_new` was an array and `x_list` a ragged list of a scalar plus arrays. The two plotting cells that follow then died with `ValueError: setting an array element with a sequence … inhomogeneous shape`. Keeping the step size a scalar keeps the whole demo scalar, as it reads. |
| `demo/02_Multi-layer_Perceptron.ipynb` | Marsland book link `seat.massey.ac.nz/personal/s.r.marsland/MLbook.html` → `homepages.ecs.vuw.ac.nz/~marslast/MLbook.html` | The Massey page is gone; the author's current page at Victoria University of Wellington serves the same book (verified 200). |
| `demo/03_Gentle_DNN.ipynb` | `filename = 'my_fun'` → `filename = 'my_fun.weights.h5'` | Keras 3 requires the `.weights.h5` suffix for `save_weights`/`load_weights`; the bare TF1 checkpoint prefix is a `ValueError`. |
| `demo/03_Gentle_DNN.ipynb` | Kaggle link `kaggle.com/zalando-research/fashionmnist` → `kaggle.com/datasets/zalando-research/fashionmnist` | Old form only redirects; the canonical `/datasets/` URL is what Kaggle serves now. |
| `demo/approx_analytical_function.py` | `filename = "mymodel"` → `"mymodel.weights.h5"` | Same Keras 3 `save_weights` suffix rule. |
| `demo/approx_analytical_function.py` | Script body wrapped in `if __name__ == "__main__":` (imports and the module docstring stay at top level) | Importing the module used to train two networks for 10 epochs each as a side effect. `python approx_analytical_function.py` behaves exactly as before. |
| `demo/checkpoint`, `demo/my_fun.index`, `demo/my_fun.data-00000-of-00001` | Deleted | Stale TensorFlow 1 checkpoint files left from a 2020 run of `03_Gentle_DNN.ipynb`. Keras 3 cannot read them and the notebook now writes `my_fun.weights.h5` instead. |
| all notebooks | `kernelspec` checked; all already `name: python3`, nothing changed | — |

`demo/mnist.pkl.gz` ships and loads as it is: `02_Multi-layer_Perceptron.ipynb` already reads it
with `pickle.load(f, encoding='iso-8859-1')`, so no Python 3 pickle fix was needed.

Notebook outputs were left untouched — none of the fixes above required re-executing a notebook
in place.

## Verification

Python 3.12.12 mirror of the 2026 student image (NumPy 2.5.3, pandas 3.0.5, scikit-learn 1.9.0,
TensorFlow 2.21.0, Keras 3.15.1, CPU only). Notebooks executed end to end with `nbclient` from
their own folder, 300 s cell timeout; scripts checked by import from their folder.

| Item | Before | After | Verified |
| --- | --- | --- | --- |
| `demo/01_GradientDescent_and_StochasticGradientDescent.ipynb` | fails — `ValueError: … inhomogeneous shape` in the adaptive-step plot cell | runs end to end | OK |
| `demo/02_Multi-layer_Perceptron.ipynb` | runs | runs (dead book link repaired) | OK |
| `demo/03_Gentle_DNN.ipynb` | fails — `save_weights` filename rejected by Keras 3 | runs end to end | OK |
| `demo/approx_analytical_function.py` | import trains two networks | imports instantly, `__main__` unchanged | IMPORT OK |
| `demo/mlp.py` | — | unchanged | IMPORT OK |
| `demo/pcn.py` | — | unchanged | IMPORT OK |

Nothing in lecture 7 is left broken.
