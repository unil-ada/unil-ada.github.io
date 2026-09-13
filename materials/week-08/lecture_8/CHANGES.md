# lecture_8 — 2026 refresh

**Source:** Simon Scheidegger's 2025 ADA lecture 8 demos and finger exercises (notebooks, scripts,
data, slides), vendored into this repo and edited in place for the 2026 student image
(Python 3.12, NumPy 2.5, pandas 3.0, TensorFlow 2.21 / Keras 3.15, PyTorch 2.14).

## Changes

| File | Change | Why |
| --- | --- | --- |
| `demo/03_Gentle_DNN.ipynb` | `filename = 'my_fun'` → `filename = 'my_fun.weights.h5'` | Keras 3 requires the `.weights.h5` suffix for `save_weights`/`load_weights`. |
| `demo/04_TF_tour.ipynb` | In the custom `r_square` metric, added `y_true = tf.cast(y_true, y_pred.dtype)` as the first line | Keras 3 hands the metric `y_true` in the dtype it was given (float64 here), `y_pred` in the model dtype (float32); `tf.square(y_true - y_pred)` is then a dtype `InvalidArgumentError`. |
| `demo/04_TF_tour.ipynb` | The Lending Club guard cell now untars `data.tar.gz` into `./data` when that folder is absent (`import tarfile` added to the import cell) | The notebook only ever *checked* for `data/LCx.csv` and `data/LCy.csv` and silently skipped the whole real-world section — there was no untar cell. The archive ships next to the notebook, so the section now runs out of the box; the `if data_untared:` guards are kept so the notebook still degrades gracefully. |
| `demo/04_TF_tour.ipynb` | Removed the commented line `#from tb_cscs import tensorboard #to use tensorboard on CSCS` | Points at infrastructure (CSCS) the course no longer uses, and at a module that has been deleted. |
| `demo/tb_cscs.py` | Deleted | CSCS-specific TensorBoard launcher for a cluster the course no longer runs on. |
| `demo/notebooks_tensorboard-jupyter-tf-2.2.0.ipynb` | `from tb_cscs import tensorboard` → `import tensorboard` | This was the one *live* reference to the deleted module (the reference in `04_TF_tour` was commented out). The plain package provides the same `tensorboard.notebook` API. |
| `demo/notebooks_tensorboard-jupyter-tf-2.2.0.ipynb` | Added `%reload_ext tensorboard` above the `%tensorboard --logdir logs` cell | Without it the cell dies with `UsageError: Line magic function %tensorboard not found` — the magic is only registered by loading the extension (`04_TF_tour.ipynb` already did this). |
| `demo/05b_Weather_data.ipynb` | `csv_path, _ = os.path.splitext(zip_path)` → `csv_path = os.path.join(zip_path, 'jena_climate_2009_2016.csv')` | Keras 3's `get_file(extract=True)` returns the extraction **directory** (`~/.keras/datasets/jena_climate_2009_2016_extracted/`), not the archive path, so the old `splitext` produced a path that does not exist. |
| `demo/Simple Regression.png`, `demo/Complex Regression.png`, `demo/Simple Classification.png`, `demo/Complex  Classification.png`, `demo/Lending Club data.png` | Deleted | Pre-rendered `plt.savefig` outputs of `04_TF_tour.ipynb`; no markdown cell references them, and the notebook writes them afresh on every run. |
| `demo/sp_und.tar.xz` | Deleted | Archive containing exactly one file, `sp_und.csv`, which sits uncompressed next to it and is what `05_RNN_intro.ipynb` reads. |
| `demo/approx_analytical_function.py` | `filename = "mymodel"` → `"mymodel.weights.h5"`; script body wrapped in `if __name__ == "__main__":` | Same Keras 3 suffix rule; and importing the module used to train two networks as a side effect. Byte-identical to the lecture 7 copy, kept in sync. |
| `Finger_exercises/01_RNN_torch.ipynb` | Renamed to `01_RNN_recap.ipynb` | `finger_exercises_lecture_8.pdf` refers to it as `01_RNN_recap.ipynb`; students could not find the file. Nothing in the repo referenced the old name. |
| `Finger_exercises/04_LSTM.ipynb` | Added a "Prerequisites" markdown cell naming the two missing pieces | The exercise needs `nltk` (not in the course environment) and the ~0.5 GB Amazon reviews archive from Kaggle unpacked into `04_data/`; neither ships. Previously it just died on `import nltk`. No code changed. |
| `demo/logs/LC/` | Kept | The `%tensorboard --logdir logs/LC` cell at the end of `04_TF_tour.ipynb` reads it. |
| all notebooks | `kernelspec` checked; all already `name: python3`, nothing changed | — |

Notebook outputs were left untouched: every notebook was executed into a throwaway copy, so the
stored 2025 outputs are unchanged. Run artefacts produced by the verification runs (`data/`,
`__pycache__/`, `my_fun.weights.h5`, `nas_outputs/`, fresh `logs/` event files, regenerated PNGs)
were removed again.

## Verification

Python 3.12.12 mirror of the 2026 student image (NumPy 2.5.3, pandas 3.0.5, scikit-learn 1.9.0,
TensorFlow 2.21.0, Keras 3.15.1, PyTorch 2.14, CPU only). Notebooks executed end to end with
`nbclient` from their own folder, 300 s cell timeout; scripts checked by import from their folder.

| Item | Before | After | Verified |
| --- | --- | --- | --- |
| `demo/03_Gentle_DNN.ipynb` | fails — `save_weights` filename rejected by Keras 3 | runs end to end | OK |
| `demo/04_TF_tour.ipynb` | fails — `r_square` dtype error; Lending Club section silently skipped | runs end to end, Lending Club section trains (new `logs/LC` event files confirmed it, then removed) | OK |
| `demo/05_RNN_intro.ipynb` | runs | unchanged | OK |
| `demo/05b_Weather_data.ipynb` | fails — `read_csv` on a non-existent path | runs end to end | OK |
| `demo/approx_analytical_function.ipynb` | runs | unchanged | OK |
| `demo/Intro_to_PyTorch.ipynb` | runs | unchanged | OK |
| `demo/notebooks_tensorboard-jupyter-tf-2.2.0.ipynb` | fails — `No module named 'tb_cscs'`, then `%tensorboard` magic missing | runs end to end | OK |
| `demo/simple_nas_random_search_10d.ipynb` | runs | unchanged | OK |
| `demo/approx_analytical_function.py` | import trains two networks | imports instantly | IMPORT OK |
| `demo/data.py` | — | unchanged | IMPORT OK |
| `demo/plot_function.py` | — | unchanged | IMPORT OK |
| `Finger_exercises/01_RNN_recap.ipynb` | runs (under the wrong filename) | runs | OK |
| `Finger_exercises/02_LSTM_basics.ipynb` | runs | unchanged | OK |
| `Finger_exercises/03_LSTM_stock.ipynb` | runs (reads `SBUX.csv`, which ships) | unchanged | OK |
| `Finger_exercises/04_LSTM.ipynb` | `ModuleNotFoundError: No module named 'nltk'` | same — **not fixable in place** | FAIL (documented) |

### Not fixable in place

`Finger_exercises/04_LSTM.ipynb` cannot run anywhere in this repo:

* `ModuleNotFoundError: No module named 'nltk'` on the first cell — `nltk` is not part of the
  2026 student image;
* the next cell needs `04_data/train.ft.txt.bz2` and `04_data/test.ft.txt.bz2` (the Amazon
  reviews dataset, ~0.5 GB behind a Kaggle login), which are not in the repo and are not
  redistributable.

Both are environment/data decisions, not code bugs, so the notebook now states them up front
instead of failing with a bare traceback. Adding `nltk` to the course environment plus a data
download step would make it run.
