from shapely.geometry import Point, Polygon
import numpy as np
import geopandas
import matplotlib.path as mpltPath
import datetime
import pandas as pd



def label_Classes(input, shapes, column_name, output):
    '''
    This function append the "Label" Column to the input Pointcloud (.txt) by checking which points are within the given polygons
    seperator in input txt : tabulator
    Columns must be Named (X,Y,Z,...)
    :param input: pointclout (.txt)
    :param shapes: polygons (.shp)
    :param column_name:
    :param output: new pointcloud (.txt)
    :return:
    '''

    pc_txt = input
    crater_poly = shapes
    output = output
    column = column_name

    pc = pd.read_csv(pc_txt, sep='\t')
    pc = pc.rename(columns = {'//X': 'X'})
    print(datetime.datetime.now(), 'Starting with File: ', pc_txt)
    shapes = geopandas.read_file(crater_poly)
    pointList = []

    # read polygon shape file and save as a list of geometries
    g = [i for i in shapes.geometry]
    l = [row[column] for index, row in shapes.iterrows()]
    polys = []
    count = 0
    for i in range(len(g)):
        count += 1
        x,y = g[i].exterior.coords.xy
        coords = np.dstack((x,y)).tolist()
        polys.append([coords, l[i]])

    #create list of all points in 2D
    for index,row in pc.iterrows():
        x= row['X']
        y= row['Y']
        pointList.append([x,y])

    #check if points are in polygons and append 0-1 lables to df
    resultsList = []
    labelList = [0] * len(pointList)
    labelArray = np.array(labelList)
    for poly in polys:

        label = poly[1]
        path = mpltPath.Path(poly[0][0])
        single_result = path.contains_points(pointList)
        single_array = np.array(single_result)
        resultsList.append(single_array*label)
        #labelList = [label if single_result[x] == True else labelList[x] for x in range(len(single_result))]
        '''
        for i in range(len(single_result)):
            if single_array[i] == True:
                labelArray[i] = label
        '''
    #labelArray = np.array(labelList)
    resultsArray = np.array(resultsList)
    final_results = sum([array for array in resultsArray])
    pc['Label'] = final_results

    print(pc.head())

    # removes higher values from overlapping polygons
    #pc.loc[pc['Label'] > 1,'Label'] = 1


    pc.to_csv(output, sep='\t')
    print('done')



def label_IDs(input, shapes, output):
    '''
    This function append the "Label" Column to the input Pointcloud (.txt) by checking which points are within the given polygons
    seperator in input txt : tabulator
    Columns must be Named (X,Y,Z,...)
    :param input: pointclout (.txt)
    :param shapes: polygons (.shp)
    :param column_name:
    :param output: new pointcloud (.txt)
    :return:
    '''

    pc_txt = input
    crater_poly = shapes
    output = output
    #column = column_name

    pc = pd.read_csv(pc_txt, sep='\t')
    pc = pc.rename(columns = {'//X': 'X'})
    print(datetime.datetime.now(), 'Starting with File: ', pc_txt)
    shapes = geopandas.read_file(crater_poly)
    pointList = []

    # read polygon shape file and save as a list of geometries
    g = [i for i in shapes.geometry]
    #l = [row[column] for index, row in shapes.iterrows()]
    polys = []
    count = 0
    for i in range(len(g)):
        count += 1
        x,y = g[i].exterior.coords.xy
        coords = np.dstack((x,y)).tolist()
        polys.append(coords)

    #create list of all points in 2D
    for index,row in pc.iterrows():
        x= row['X']
        y= row['Y']
        pointList.append([x,y])

    #check if points are in polygons and append 0-1 lables to df
    resultsList = []
    labelList = [0] * len(pointList)
    labelArray = np.array(labelList)
    count = 0
    for poly in polys:

        label = count
        path = mpltPath.Path(poly[0])
        single_result = path.contains_points(pointList)
        single_array = np.array(single_result)
        resultsList.append(single_array*label)
        #labelList = [label if single_result[x] == True else labelList[x] for x in range(len(single_result))]
        '''
        for i in range(len(single_result)):
            if single_array[i] == True:
                labelArray[i] = label
        '''
    #labelArray = np.array(labelList)
    resultsArray = np.array(resultsList)
    final_results = sum([array for array in resultsArray])
    pc['Label'] = final_results
    print(pc.head())

    # removes higher values from overlapping polygons
    #pc.loc[pc['Label'] > 1,'Label'] = 1

    pc.to_csv(output, sep='\t')
    print('done')


def label_Ones(input, shapes, output):
    '''
    This function append the "Label" Column to the input Pointcloud (.txt) by checking which points are within the given polygons
    seperator in input txt : tabulator
    Columns must be Named (X,Y,Z,...)
    :param input: pointclout (.txt)
    :param shapes: polygons (.shp)
    :param output: new pointcloud (.txt)
    :return:
    '''

    pc_txt = input
    crater_poly = shapes
    output = output

    pc = pd.read_csv(pc_txt, sep='\t')
    pc = pc.rename(columns = {'//X': 'X'})
    print(datetime.datetime.now(), 'Starting with File: ', pc_txt)
    shapes = geopandas.read_file(crater_poly)
    pointList = []

    # read polygon shape file and save as a list of geometries
    g = [i for i in shapes.geometry]
    polys = []
    count = 0
    for i in range(len(g)):
        count += 1
        x,y = g[i].exterior.coords.xy
        coords = np.dstack((x,y)).tolist()
        polys.append([coords, 1])

    #create list of all points in 2D
    for index,row in pc.iterrows():
        x= row['X']
        y= row['Y']
        pointList.append([x,y])

    #check if points are in polygons and append 0-1 lables to df
    resultsList = []
    labelList = [0] * len(pointList)
    labelArray = np.array(labelList)
    for poly in polys:

        label = poly[1]
        path = mpltPath.Path(poly[0][0])
        single_result = path.contains_points(pointList)
        single_array = np.array(single_result)
        resultsList.append(single_array*label)
        #labelList = [label if single_result[x] == True else labelList[x] for x in range(len(single_result))]
        '''
        for i in range(len(single_result)):
            if single_array[i] == True:
                labelArray[i] = label
        '''
    #labelArray = np.array(labelList)
    resultsArray = np.array(resultsList)
    final_results = sum([array for array in resultsArray])
    pc['Label'] = final_results

    print(pc.head())

    # removes higher values from overlapping polygons
    pc.loc[pc['Label'] > 1,'Label'] = 1

    #pc = pc.drop([pc.columns[0]], axis = 1)
    print(pc.columns.values)
    pc = pc.drop([pc.columns[0]], axis = 1)
    pc.to_csv(output, sep='\t')
    print('done')

