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


def most_frequent(List):
    counter = 0
    num = List[0]

    for i in List:
        curr_frequency = List.count(i)
        if (curr_frequency > counter):
            counter = curr_frequency
            num = i

    return num


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
        paramList.append([float(line[i]) for i in range(5,35)])
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

dir = 'models'
predictionList = []
count = 0


# load all models
modellist = []
for file in os.listdir(dir):
    filename = os.path.join(dir, file)
    loaded_model = pickle.load(open(filename, 'rb'))
    modellist.append(loaded_model)
print('models loaded')
print(modellist[:5])
for i in range(len(xyzArray)):
    point = xyzArray[i]
    params = pd.DataFrame(data=paramArray[i]).T
    params = params.dropna(axis=0, how ='any')
    results = []
    if len(params)>0:
        for model in modellist:
            result = model.predict(params)
            results.append(result)

    predictionList.append(most_frequent(results))
    count += 1
    if count % 100000 == 0:
        print(count)

predictionArray= np.array(predictionList)


fobj_lans = open("txt_files/prediction_multiple_trees.txt", 'w')
for i in range(len(xyzArray)):

    fobj_lans.write("%1.3f\t%1.3f\t%1.3f\t%1.3f\n" %(float(xyzArray[i]), float(xyzArray[i]), float(xyzArray[i]), float(predictionArray[i])))

print('done')

fobj_lans.close()

