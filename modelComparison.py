# Basic imports
import os
import re
import pandas as pd
import numpy as np
import pickle

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

filter = ['X', 'Y' ,'Z', 'Label' ,'Roughness (12)' ,'Mean curvature (12)',
         'Gaussian curvature (12)', 'Normal change rate (12)',
         'Number of neighbors (r=12)', 'Surface density (r=12)',
         'Volume density (r=12)', 'Planarity (12)' ,'Linearity (12)',
         'Surface variation (12)' ,'Sphericity (12)', 'Roughness (6)',
         'Mean curvature (6)', 'Gaussian curvature (6)', 'Normal change rate (6)',
         'Number of neighbors (r=6)', 'Surface density (r=6)',
         'Volume density (r=6)', 'Anisotropy (6)', 'Planarity (6)', 'Linearity (6)',
         'Surface variation (6)', 'Sphericity (6)' ,'Roughness (3)',
         'Mean curvature (3)' ,'Gaussian curvature (3)' ,'Normal change rate (3)',
         'Number of neighbors (r=3)', 'Surface density (r=3)',
         'Volume density (r=3)', 'Anisotropy (3)' ,'Planarity (3)', 'Linearity (3)',
         'Surface variation (3)' ,'Sphericity (3)']



# Read the data, remove the 'neutral' label and change -1 to 0 because only idiots use negative integers for labels
my_data_Lans = pd.read_csv('txt_files/Labeled_Training_Data_Lans.txt', sep='\t')
my_data_Natters = pd.read_csv('txt_files/Labeled_Training_Data_Lans.txt', sep='\t')
my_data_test = pd.read_csv('txt_files/Test_Clip_Lans_parameter.txt', sep='\t')

my_data_Lans = my_data_Lans.filter(items= filter)
my_data_Natters = my_data_Natters.filter(items= filter)
my_data_test = my_data_test.filter(items= filter)

my_data = pd.concat([my_data_Lans, my_data_Natters])
my_data = my_data.dropna(axis=0, how='any')
my_data_test = my_data_test.dropna(axis=0, how='any')

# Split the data into one list containing the tweets and one containing the labels
my_labels = my_data['Label'].values.tolist()
my_data = my_data.drop(['Label'], axis=1)

print('len my_data: ', len(my_data.columns.values))

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

filename = 'finalized_tree_model.sav'
pickle.dump(my_tree_mod, open(filename, 'wb'))


# Create random forest
my_forest_mod = RandomForestClassifier(criterion = 'gini', n_estimators = 500)
my_forest_mod.fit(X_train, y_train)
# Predict validation data and compute accuracy
my_forest_mod_acc = accuracy_score(y_val, my_forest_mod.predict(X_val))
print('Random forest accuracy:', my_forest_mod_acc)

filename = 'finalized_forest_model.sav'
pickle.dump(my_forest_mod, open(filename, 'wb'))

prediction = my_forest_mod.predict(my_data_test)

predictionArray = np.array(prediction)
fobj_lans = open("txt_files/Test_Clip_Lans_predicted_forest.txt", 'w')

for index, row in my_data_test.iterrows():

    fobj_lans.write("%1.3f\t%1.3f\t%1.3f\t%1.3f\n" %(float(row['X']), float(row['Y']), float(row['Z']), float(predictionArray[index-1])))

print('done tree')

fobj_lans.close()

prediction = my_forest_mod.predict(my_data)

predictionArray = np.array(prediction)
fobj_lans = open("txt_files/Test_Clip_Lans_predicted_forest_2.txt", 'w')

for index, row in my_data.iterrows():

    fobj_lans.write("%1.3f\t%1.3f\t%1.3f\t%1.3f\n" %(float(row['X']), float(row['Y']), float(row['Z']), float(predictionArray[index-1
                                                                                                              ])))

print('done tree')

fobj_lans.close()

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