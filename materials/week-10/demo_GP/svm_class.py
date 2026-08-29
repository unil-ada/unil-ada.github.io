import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score,accuracy_score


########################################################################

# load data
cars = pd.read_csv('auto-mpg.data.txt',header=None, sep='\s+')

## Extract Power and Weight as matrix
X = cars.iloc[:, [3,4]].values

## Origin of Car
y = [1 if o==1 else 0 for o in cars.iloc[:, 7].values]

# split into training data (80%) and test data (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# Standardize
scaler = StandardScaler()
scaler.fit(X_train)
X_train_standardized = scaler.transform(X_train)
X_test_standardized = scaler.transform(X_test)

# train SVM
svm = SVC(kernel='linear', C=1.0, random_state=0)
svm.fit(X_train,y_train)
y_predicted = svm.predict(X_test_standardized)
# Confusion Matrix
print("Confusion Matrix:\n", confusion_matrix(y_true=y_test, y_pred=y_predicted))
## 
print("Accuracy :\n", accuracy_score(y_true=y_test, y_pred=y_predicted))
