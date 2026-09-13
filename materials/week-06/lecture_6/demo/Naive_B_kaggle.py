"""
Naive Bayes Sentiment Classification on Amazon Unlocked Mobile Reviews
---------------------------------------------------------------------

This script demonstrates a basic text classification pipeline using
the Multinomial Naive Bayes model in scikit-learn. It performs the following steps:

1. **Data loading**: Reads the dataset `Amazon_Unlocked_Mobile.csv` containing
   product reviews and star ratings.

2. **Preprocessing**: 
   - Extracts review texts and corresponding labels.
   - Removes missing entries.

3. **Vectorization**:
   - Converts textual data into a bag-of-words representation using `CountVectorizer`.

4. **Model training**:
   - Splits data into training (80%) and testing (20%) sets.
   - Fits a `MultinomialNB` classifier with a small smoothing parameter (alpha = 1e-10).

5. **Evaluation**:
   - Predicts ratings on the test data.
   - Computes and prints the confusion matrix and overall accuracy.

6. **Model interpretation**:
   - Displays the class priors (probabilities of each rating).
   - For a few selected words, prints the per-class conditional probabilities
     (how likely each word is under each rating class).

The script uses the current scikit-learn API (`get_feature_names_out`) and 
efficient vocabulary lookup through `vectorizer.vocabulary_`.

DATA (required -- the script does nothing without it)
-----------------------------------------------------
The dataset is `Amazon_Unlocked_Mobile.csv` (~130 MB uncompressed). It is not
redistributable, so it is not part of the course repository. Get it from Kaggle
(a free Kaggle account / login is required):

    https://www.kaggle.com/datasets/PromptCloudHQ/amazon-reviews-unlocked-mobile-phones

Put `Amazon_Unlocked_Mobile.csv` -- or the downloaded
`amazon-reviews-unlocked-mobile-phones.zip`, which the script unpacks for you --
in this same folder (next to this script), then run it from this folder:

    python Naive_B_kaggle.py

Without that file the script prints these instructions and exits; it has no
fallback dataset.

Author: [Your Name]
Institution: University of Lausanne / Yale / MIT / UPenn
Date: October 2025
"""

import math
import sys
import zipfile
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix, accuracy_score

# ----------------------------
# Load data
# ----------------------------
HERE = Path(__file__).resolve().parent
CSV_NAME = "Amazon_Unlocked_Mobile.csv"
ZIP_NAME = "amazon-reviews-unlocked-mobile-phones.zip"
KAGGLE_URL = (
    "https://www.kaggle.com/datasets/PromptCloudHQ/"
    "amazon-reviews-unlocked-mobile-phones"
)

csv_path = HERE / CSV_NAME
zip_path = HERE / ZIP_NAME

if not csv_path.exists() and zip_path.exists():
    print(f"Unpacking {ZIP_NAME} (this takes a moment, the CSV is ~130 MB) ...")
    with zipfile.ZipFile(zip_path) as zf:
        zf.extract(CSV_NAME, path=HERE)

if not csv_path.exists():
    sys.exit(
        f"\nMissing data file: {csv_path}\n"
        f"\nThis script needs the Kaggle dataset 'Amazon Reviews: Unlocked Mobile Phones'."
        f"\nDownload it (free Kaggle account required) from:\n  {KAGGLE_URL}\n"
        f"\nThen put '{CSV_NAME}' (or the downloaded '{ZIP_NAME}') in:\n  {HERE}\n"
        f"\nand run this script again from that folder. Nothing else to do -- "
        f"there is no fallback dataset, so the script stops here.\n"
    )

reviews = pd.read_csv(csv_path, encoding="utf-8")

# Text is column 4, labels (ratings) are column 3 in this dataset layout
X_raw = reviews.iloc[:, 4]
y_raw = reviews.iloc[:, 3]

# Keep only rows where the text is not NaN, and align y accordingly
mask = X_raw.notna()
X_clean = X_raw[mask]
y_clean = y_raw[mask]

# ----------------------------
# Vectorize (bag of words)
# ----------------------------
vectorizer = CountVectorizer()
X_cnt = vectorizer.fit_transform(X_clean)

# ----------------------------
# Train/test split
# ----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X_cnt, y_clean, test_size=0.2, random_state=0
)

# ----------------------------
# Train Naive Bayes
# ----------------------------
# Note: extremely small alpha may underflow on some setups; keeping your choice.
nb = MultinomialNB(alpha=1e-10)
nb.fit(X_train, y_train)

# ----------------------------
# Evaluate
# ----------------------------
y_predicted = nb.predict(X_test)
print(confusion_matrix(y_true=y_test, y_pred=y_predicted))
print(accuracy_score(y_true=y_test, y_pred=y_predicted))

# ----------------------------
# Class priors (in probability space)
# ----------------------------
for c in range(len(nb.classes_)):
    print("Class:", nb.classes_[c])
    print(math.exp(nb.class_log_prior_[c]))

# ----------------------------
# Feature names (new API) and per-class word probabilities
# ----------------------------
feature_names = vectorizer.get_feature_names_out()
vocab = vectorizer.vocabulary_

words = ["android", "apple", "good", "bad", "terrible", "error", "crash"]
for w in words:
    idx = vocab.get(w, None)
    if idx is None:
        print(f"Word '{w}' not found in the vocabulary.")
        continue

    print("Word:", w)
    for c in range(len(nb.classes_)):
        prob = math.exp(nb.feature_log_prob_[c][idx])
        print(f"{nb.classes_[c]} : {prob}")
