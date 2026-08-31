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

Author: [Your Name]
Institution: University of Lausanne / Yale / MIT / UPenn
Date: October 2025
"""

import math
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix, accuracy_score

# ----------------------------
# Load data
# ----------------------------
reviews = pd.read_csv("Amazon_Unlocked_Mobile.csv", encoding="utf-8")

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
