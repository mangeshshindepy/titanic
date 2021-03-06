# -------------------------> Importing the required Libraries ------------------------------

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import cross_val_score
from sklearn.metrics import confusion_matrix

# -------------------------> Getting the Dataset -------------------------------------------

data = pd.read_csv('train.csv')
data_test = pd.read_csv('test.csv')

# -------------------------> Finding the percentage of missing values ----------------------

missing = []

for i in data.columns:
  missing.append([i, data[i].isnull().sum()/len(data) * 100])
  
# -------------------------> Removing unnecessary data -------------------------------------
  
data.drop(['PassengerId', 'Name', 'Ticket', 'Cabin', 'Embarked'], axis = 1, inplace = True)
data_test.drop(['PassengerId', 'Name', 'Ticket', 'Cabin', 'Embarked'], axis = 1, inplace = True)

# -------------------------> Filling the null values with the mode -------------------------

data.fillna(data.mode().iloc[0], inplace = True)
data_test.fillna(data.mode().iloc[0], inplace = True)

# -------------------------> Getting the Dummy Variables -----------------------------------

data = pd.get_dummies(data, drop_first = True)
data_test = pd.get_dummies(data_test, drop_first = True)

# -------------------------> Labelling training and test set -----------------------------

X = data.drop('Survived', axis = 1)
y = data['Survived']
X_test1 = data_test
for i in ['Pclass', 'SibSp', 'Parch']:
  X[i] = X[i].astype('category')

# -------------------------> Splitting data ----------------------------------------------

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

# -------------------------> Log transforming Age and Fare --------------------------------

#X_train[['Age', 'Fare']] = np.log(X_train[['Age', 'Fare']])
#X_test[['Age', 'Fare']] = np.log(X_test[['Age', 'Fare']])

# -------------------------> Visualizing the data ----------------------------------------

sns.barplot(x = 'Sex_male', y = 'Survived', data = data, hue = 'Pclass')
sns.boxplot(x = 'Pclass', y = 'Age', data = data, hue = 'Sex_male')
sns.heatmap(data.corr())
sns.boxplot(x = 'Survived', y = 'Age', data = data, hue = 'Sex_male')

# --------------------------> Implemeting models ----------------------------------------

## Logistic Regression

from sklearn.linear_model import LogisticRegression
classifier1 = LogisticRegression()
classifier1.fit(X_train, y_train)

score1 = cross_val_score(estimator = classifier1, X =  X_train, y = y_train, cv = 10)
print(score1.mean())

y_pred = classifier1.predict(X_test)

## Stochastic Gradient Classifier

from sklearn.linear_model import SGDClassifier
classifier2 = SGDClassifier(random_state = 0, n_jobs = -1)
classifier2.fit(X_train, y_train)

score2 = cross_val_score(estimator = classifier2, X =  X_train, y = y_train, cv = 10)
print(score2.mean())

y_pred = classifier2.predict(X_test)

## Random Forest Classifier 

from sklearn.ensemble import RandomForestClassifier
classifier3 = RandomForestClassifier(n_estimators = 300, random_state = 0)
classifier3.fit(X_train,y_train)

score3 = cross_val_score(estimator = classifier3, X = X_train, y = y_train, cv = 10)
print(score3.mean())

y_pred = classifier3.predict(X_test)

## Support Vector Classifier

from sklearn.svm import SVC
classifier4 = SVC(kernel = 'rbf', random_state = 0)
classifier4.fit(X_train, y_train)

score4 = cross_val_score(estimator = classifier4, X = X_train, y = y_train, cv = 10)
print(score4.mean())

y_pred = classifier4.predict(X_test)

cm4 = confusion_matrix(y_test, y_pred)

## Naive Bayes Classifier

from sklearn.naive_bayes import GaussianNB
classifier5 = GaussianNB()
classifier5.fit(X_train, y_train)

score5 = cross_val_score(estimator = classifier5, X = X_train, y = y_train, cv = 10)
print(score5.mean())

y_pred = classifier5.predict(X_test)

cm4 = confusion_matrix(y_test, y_pred)

## Bagging Classifier

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import BaggingClassifier
classifier6 = BaggingClassifier(base_estimator = DecisionTreeClassifier(random_state = 0), 
                                n_estimators = 300, n_jobs = -1)
classifier6.fit(X_train, y_train)

score6 = cross_val_score(estimator = classifier6, X = X_train, y = y_train, cv = 10)
print(score6.mean())

y_pred = classifier6.predict(X_test)
y_pred1 = classifier6.predict(X_test1)

cm6 = confusion_matrix(y_test, y_pred)

## Adaptive Boost Algorithm

from sklearn.ensemble import AdaBoostClassifier
classifier7 = AdaBoostClassifier(base_estimator = DecisionTreeClassifier(), 
                                 n_estimators = 500, learning_rate = 0.1, 
                                 random_state = 0)
classifier7.fit(X_train, y_train)

score7 = cross_val_score(estimator = classifier7, X = X_train, y = y_train, cv = 10)
print(score7.mean())

y_pred = classifier7.predict(X_test)

cm7 = confusion_matrix(y_test, y_pred)

## Gradient Boosting Algorithm

from sklearn.ensemble import GradientBoostingClassifier
classifier8 = GradientBoostingClassifier(learning_rate = 0.01, n_estimators = 1000, random_state = 0)
classifier8.fit(X_train, y_train)

score8 = cross_val_score(estimator = classifier8, X = X_train, y = y_train, cv = 10)
print(score8.mean())

y_pred = classifier8.predict(X_test)

cm8 = confusion_matrix(y_test, y_pred)

parameter = [{'learning_rate' : [0.01, 0.05, 0.1],
              'n_estimators' : [100, 500, 1000],
              'min_samples_split' : [2, 4, 6],
              'max_depth' : [3, 4, 5]}]

from sklearn.grid_search import GridSearchCV
grid_search = GridSearchCV(estimator = classifier8, 
                           param_grid = parameter, scoring = 'accuracy', 
                           verbose = 10, n_jobs = -1)

grid_search.fit(X_train, y_train)

classifier8 = grid_search.best_estimator_

y_pred = classifier8.predict(X_test)
y_pred1 = classifier8.predict(X_test1)

score8 = cross_val_score(estimator = classifier8, X = X_train, y = y_train, cv = 10)
print(score8.mean())

## XGBoost Algorithm

from xgboost import XGBClassifier
classifier9 = XGBClassifier(learning_rate = 0.01, n_estimators = 1000, n_jobs = -1)
classifier9.fit(X_train, y_train)

parameter = [{'learning_rate' : [0.01, 0.05, 0.1],
              'n_estimators' : [100, 500, 1000]}]

grid_search = GridSearchCV(estimator = classifier9, 
                           param_grid = parameter, scoring = 'accuracy', 
                           verbose = 10, n_jobs = -1)

grid_search.fit(X_train, y_train)

classifier9 = grid_search.best_estimator_
  
y_pred = classifier9.predict(X_test)

cm9 = confusion_matrix(y_test, y_pred)

score9 = cross_val_score(estimator = classifier9, X = X_train, y = y_train, cv = 10)
print(score9.mean())

## Implementing Neural Network

import keras
from keras.layers import Dense
from keras.models import Sequential

classifier10 = Sequential()
classifier10.add(Dense(input_dim = 6, activation = 'relu', output_dim = 5, init = 'uniform'))
classifier10.add(Dense(activation = 'relu', output_dim = 4, init = 'uniform'))
classifier10.add(Dense(activation = 'relu', output_dim = 4, init = 'uniform'))
classifier10.add(Dense(activation = 'relu', output_dim = 3, init = 'uniform'))
classifier10.add(Dense(activation = 'sigmoid', output_dim = 1, init = 'uniform'))
classifier10.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])
classifier10.fit(X_train, y_train, batch_size = 10, nb_epoch = 100)

## Implementing the Voting Classifier

from sklearn.ensemble import VotingClassifier

voting = VotingClassifier(estimators = [('RF', classifier3),
                                         ('svc', classifier4), 
                                         ('gaussian', classifier5), 
                                         ('bagging', classifier6),
                                         ('adaboost', classifier7),
                                         ('grboost', classifier8),
                                         ('xgboost', classifier9)], n_jobs = -1)
  
voting.fit(X_train, y_train)
y_pred = voting.predict(X_test)
cm9 = confusion_matrix(y_test, y_pred)
y_pred1 = voting.predict(X_test1)