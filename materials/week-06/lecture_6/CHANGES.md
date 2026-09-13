# lecture_6 — 2026 refresh

**Source:** Simon Scheidegger's 2025 ADA lecture 6 demos (notebooks, scripts, data, slides),
vendored into this repo and edited in place for the 2026 student image
(Python 3.12, NumPy 2.5, pandas 3.0, scikit-learn 1.9, matplotlib 3.10).

## Changes

| File | Change | Why |
| --- | --- | --- |
| `demo/AdaBoost.py` | `AdaBoostClassifier(base_estimator=tree, …)` → `estimator=tree` | `base_estimator` was renamed in scikit-learn 1.2 and removed in 1.4; the old name is a `TypeError`. |
| `demo/auto_class.py` | Colour list built from `y_test` → built from `y_train` | The scatter plots the **training** points (`hp_train`, `weight_train`), so colouring them by the test labels mislabels the classes (and only works at all because the two arrays happen to have compatible lengths). |
| `demo/auto_class.py` | Swapped the two labels in the per-car printout | It printed `y_test` under "Predicted class" and `y_predicted` under "Correct class" — the wrong way round. |
| `demo/Naive_B_kaggle.py` | Header docstring now names the Kaggle source, the target folder, and says the script does nothing without the data; the loader looks for `Amazon_Unlocked_Mobile.csv`, falls back to unpacking `amazon-reviews-unlocked-mobile-phones.zip` if it is present, and otherwise `sys.exit()`s with those instructions | The 130 MB CSV needs a Kaggle login and is not redistributable. Previously the script died with a bare `FileNotFoundError` traceback. Download: <https://www.kaggle.com/datasets/PromptCloudHQ/amazon-reviews-unlocked-mobile-phones> |
| `Finger_exercises/visualization.py` | `matplotlib.cm.get_cmap(name)` → `matplotlib.colormaps[name]` (two call sites; `import matplotlib.cm as cm` → `import matplotlib as mpl`) | `cm.get_cmap` was removed in matplotlib 3.9. This also broke `05_Ensemble_Learning.ipynb`, which imports this module. |
| `Finger_exercises/01_Feature_Engineering.ipynb` | `vec.get_feature_names()` → `vec.get_feature_names_out()` (three cells) | `get_feature_names` was removed from the transformers in scikit-learn 1.2. |
| `demo/zoo_predict_aux.py` | Deleted | Byte-identical orphan copy of `demo/zoo/zoo_predict_aux.py`; nothing imports or runs it, and it could not work where it sat because `zoo_data.txt` lives in `demo/zoo/`. |
| `demo/out.txt`, `demo/tree.dot`, `demo/tree.pdf`, `demo/MSE.png` | Deleted | Run artefacts from an old session; grepped, nothing reads them. (`tree.dot` is written afresh by `auto_tree.py` / `auto_tree_simple.py` each run; `tree.pdf` is what the comment in `auto_tree.py` tells you to produce from it with `dot`.) |
| all notebooks | `kernelspec` checked; all already `{"name": "python3", "display_name": "Python 3"}`, nothing changed | — |

No notebook outputs were changed: none of the fixes above are inside a notebook that needed
re-executing to stay consistent (`01_Feature_Engineering.ipynb` and `05_Ensemble_Learning.ipynb`
were verified by execution but their stored outputs were left as they were).

## Verification

`python 3.12.12` from the 2026 image mirror. Notebooks executed with `nbclient` from their own
folder (300 s cell timeout); scripts run as `python X.py` from their folder (120 s), `MPLBACKEND=Agg`.

| Item | Result |
| --- | --- |
| `demo/auto_class_knn.ipynb` | OK |
| `Finger_exercises/01_Feature_Engineering.ipynb` | OK (after the `get_feature_names_out` fix) |
| `Finger_exercises/02_knn_classifier.ipynb` | OK |
| `Finger_exercises/03a_prior_information_entropy.ipynb` | OK |
| `Finger_exercises/03b_hands_on_entropy.ipynb` | OK |
| `Finger_exercises/03c_DecisionTrees.ipynb` | OK |
| `Finger_exercises/04_Naive_Bayes.ipynb` | OK |
| `Finger_exercises/05_Ensemble_Learning.ipynb` | OK (after the `visualization.py` colormap fix) |
| `demo/AdaBoost.py` | OK — accuracy 0.671 |
| `demo/auto_class.py` | OK — 58 correct / 21 incorrect |
| `demo/auto_class_knn.py` | OK |
| `demo/auto_tree.py`, `demo/auto_tree_simple.py` | OK (each rewrites `tree.dot`) |
| `demo/bagging.py` | OK — accuracy 0.696 |
| `demo/CompQualityMeasures.py` | OK |
| `demo/entropy.py` | OK |
| `demo/majority.py` | OK (logistic regression emits a `ConvergenceWarning` at the default `max_iter=100`; pre-existing, not fatal) |
| `demo/Naive_B_kaggle.py` | OK with the data present (unpacked from the bundled zip); with the data absent it exits cleanly with the download instructions |
| `demo/sklearn_lda.py` | OK |
| `demo/zoo/zoo_predict.py`, `demo/zoo/zoo_predict_aux.py` | OK — accuracy 80.95 % |
| `Finger_exercises/helpers_05_08.py` | OK (imports cleanly) |
| `Finger_exercises/visualization.py` | OK (after the colormap fix; emits a `FutureWarning` about `SVC(probability=True)` deprecated in sklearn 1.9 — cosmetic for now, will need `CalibratedClassifierCV` before 1.11) |

Nothing left unfixed.
