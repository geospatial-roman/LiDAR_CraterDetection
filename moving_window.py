# Basic imports
import os
import pandas as pd
import numpy as np
import pickle
import datetime

# KDtree import
from sklearn.neighbors import KDTree

# Sk Learn ML imports
from sklearn import preprocessing
from sklearn import tree
from sklearn.metrics import confusion_matrix
from matplotlib import pyplot as plt

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

'''
# Load data sets
my_data_Lans = pd.read_csv('txt_files/Labeled_Training_Data_Lans.txt', sep='\t')
#my_data_Natters = pd.read_csv('txt_files/Labeled_Training_Data_Natters.txt', sep='\t')

# Reduce Dataset to same Columns and concat
my_data_Lans = my_data_Lans.filter(items= filter)
#my_data_Natters = my_data_Natters.filter(items= filter)
#my_data = pd.concat([my_data_Lans,my_data_Natters])
my_data = my_data_Lans.dropna(axis=0, how='any')




#Create np Arrays for KD tree
xyzList = []
labelList = []
paramList = []

for index, row in my_data.iterrows():
    xyzList.append([row['X'], row['Y'], row['Z']])
    labelList.append(row['Label'])
    paramList.append([row['Roughness (12)'] ,row['Mean curvature (12)'],
         row['Gaussian curvature (12)'], row['Normal change rate (12)'],
         row['Number of neighbors (r=12)'], row['Surface density (r=12)'],
         row['Volume density (r=12)'], row['Planarity (12)'] ,row['Linearity (12)'],
         row['Surface variation (12)'] ,row['Sphericity (12)'], row['Roughness (6)'],
         row['Mean curvature (6)'], row['Gaussian curvature (6)'], row['Normal change rate (6)'],
         row['Number of neighbors (r=6)'], row['Surface density (r=6)'],
         row['Volume density (r=6)'], row['Anisotropy (6)'], row['Planarity (6)'], row['Linearity (6)'],
         row['Surface variation (6)'], row['Sphericity (6)'] ,row['Roughness (3)'],
         row['Mean curvature (3)'] ,row['Gaussian curvature (3)'] ,row['Normal change rate (3)'],
         row['Number of neighbors (r=3)'], row['Surface density (r=3)'],
         row['Volume density (r=3)'], row['Anisotropy (3)'] ,row['Planarity (3)'], row['Linearity (3)'],
         row['Surface variation (3)'] ,row['Sphericity (3)']])

'''
fobj = open("txt_files/Labeled_Training_Data_Lans.txt", "r")

xyzList = []
labelList = []
paramList = []
count= 0
for line in fobj:
    if count > 0:
        line = line.strip()
        line = line.split('\t')
        xyzList.append([float(line[0]), float(line[1]), float(line[2])])
        labelList.append(float(line[4]))
        paramList.append([float(line[i]) for i in range(5, 35)])
    count +=1
fobj.close()
print(str(datetime.datetime.now())[:19], ' files Opened')
print('xyz sample: ', xyzList[0])
print('label sample: ', labelList[0])
print('param sample: ', paramList[0])



xyzArray = np.array(xyzList)
labelArray = np.array(labelList)
paramArray = np.array(paramList)
print(str(datetime.datetime.now())[:19], ' array created')

# calculate KD Tree
tree3D = KDTree(xyzArray)
print(str(datetime.datetime.now())[:19], " KDtree calculated")

# iterrate through all point, check if labels points are in 10m radius and train model if so

model_list = []
for i in range(len(xyzArray)):

    #get searchPoint an neighbouring Points in x meters distance
    point = [xyzArray[i]]
    dists, idxList = tree3D.query(point, k=800)
    labels = [labelArray[j] for j in idxList[0]]

    if sum(labels) >  350:

        model_name = str('model_'+str(i))
        training_df = pd.DataFrame(data=[paramArray[j] for j in idxList[0]])

        training_df['label'] = labels
        training_df = training_df.dropna(axis=0, how='any')

        label_df = training_df.filter(items=['label'])
        training_df = training_df.drop(['label'], axis=1)


        # Create classification tree
        my_tree_mod = tree.DecisionTreeClassifier(criterion='gini')
        my_tree_mod.fit(training_df, label_df)

        # save model

        pickle.dump(my_tree_mod, open(str('models/'+model_name+'.sav'), 'wb'))
        model_list.append(model_name)
        print('model calculated: ', model_name)



