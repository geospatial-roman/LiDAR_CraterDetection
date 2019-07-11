# Basic imports
import os
import re
import pandas as pd
import numpy as np

# Sk learn preprocessors
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

# Sklearn models
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn import tree
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

'''
# Keras Käse
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Dense, Embedding, LSTM, SpatialDropout1D, Dropout, Activation, Conv1D, GlobalMaxPooling1D, BatchNormalization
from keras.callbacks import CSVLogger, EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from keras import optimizers
from keras import backend as K

# Own stuff
from models import get_base_cnn
'''
# Sklearn utility functions
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split



# Where are we?
print(os.getcwd())



# Read the data, remove the 'neutral' label and change -1 to 0 because only idiots use negative integers for labels
my_data = pd.read_csv('clip_with_param.txt', sep='\t', header=['X', 'Y', 'Z', 'intensity', 'label'])

# Split the data into one list containing the tweets and one containing the labels
my_tweets = my_data['text'].values.tolist()
my_labels = my_data['label'].values.tolist()

# Use tf-idf for even smarter preprocessing
my_tfidf = TfidfTransformer()
my_tweets = my_tfidf.fit_transform(my_tweets)

# Generate a train and val split
my_train_prop = 0.66
X_train, X_val, y_train, y_val = train_test_split(my_data, my_labels,
                                                  train_size = my_train_prop, test_size  = 1 - my_train_prop,
                                                  random_state = 1)




# Create a Naive Bayes model
my_bayes_mod = MultinomialNB(alpha = 1, fit_prior = True)
my_bayes_mod.fit(X_train, y_train)
# Predict validation data and compute accuracy
my_bayes_mod_acc = accuracy_score(y_val, my_bayes_mod.predict(X_val))
print('Naive Bayes accuracy:', my_bayes_mod_acc)

# Create a logistic regression model
my_reg_mod = LogisticRegression(penalty = 'l2', C = 1, solver = 'liblinear')
my_reg_mod.fit(X_train, y_train)
# Predict validation data and compute accuracy
my_reg_mod_acc = accuracy_score(y_val, my_reg_mod.predict(X_val))
print('Logistic regression accuracy:', my_reg_mod_acc)

# Create classification tree
my_tree_mod = tree.DecisionTreeClassifier(criterion = 'gini')
my_tree_mod.fit(X_train, y_train)
# Predict validation data and compute accuracy
my_tree_mod_acc = accuracy_score(y_val, my_tree_mod.predict(X_val))
print('Classification tree accuracy:', my_tree_mod_acc)

# Create random forest
my_forest_mod = RandomForestClassifier(criterion = 'gini', n_estimators = 500)
my_forest_mod.fit(X_train, y_train)
# Predict validation data and compute accuracy
my_forest_mod_acc = accuracy_score(y_val, my_forest_mod.predict(X_val))
print('Random forest accuracy:', my_forest_mod_acc)

# Creating a gradient boosting model
my_boosting_mod = GradientBoostingClassifier(loss = 'deviance', learning_rate = 0.01, n_estimators = 500)
my_boosting_mod.fit(X_train, y_train)
# Predict validation data and compute accuracy
my_boosting_mod_acc = accuracy_score(y_val, my_boosting_mod.predict(X_val))
print('Gradient boosting accuracy:', my_boosting_mod_acc)

# Create support vector machine
my_svm_mod = SVC(C = 100, kernel = 'rbf', gamma = 'auto')
my_svm_mod.fit(X_train, y_train)
# Predict validation data and compute accuracy
my_svm_mod_acc = accuracy_score(y_val, my_svm_mod.predict(X_val))
print('Support vector machine accuracy:', my_svm_mod_acc)