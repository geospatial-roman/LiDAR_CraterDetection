import numpy as np
import matplotlib.path as mpltPath
import datetime
import pandas as pd
from utils import read_shapes


def label_Craters(input, shapes, output):
    """
    This function append the "Label" Column to the input Pointcloud (.txt) by checking which points are within the given polygons
    seperator in input txt : tabulator
    Columns must be Named (X,Y,Z,...)
    :param input: point cloud (.txt)
    :param shapes: polygons (.shp)
    :param output: new point cloud (.txt)
    :return:
    """

    pc_txt = input
    crater_poly = shapes
    output = output

    pc = pd.read_csv(pc_txt, sep=';')
    shapes = read_shapes.read_shapefile(crater_poly)

    if 'Label' in pc.columns:
        pc = pc.drop(labels=['Label'], axis=1)
    pc = pc.rename(columns={'//X': 'X'})
    print(datetime.datetime.now(), 'Starting with File: ', pc_txt)

    pointList = []

    if 'Longitude' in shapes.columns:
        shapes = shapes.rename(columns={'Longitude': 'X'})
    if 'Lon' in shapes.columns:
        shapes = shapes.rename(columns={'Lon': 'X'})
    if 'Latitude' in shapes.columns:
        shapes = shapes.rename(columns={'Latitude': 'Y'})
    if 'Lat' in shapes.columns:
        shapes = shapes.rename(columns={'Lat': 'Y'})
    if '//X' in shapes.columns:
        shapes = shapes.rename(columns={'//X': 'X'})

    # read polygon shape file and save as a list of geometries
    polys = [[row['coords'], 1] for index, row in shapes.iterrows()]

    # create list of all points in 2D
    for index, row in pc.iterrows():
        x = row['X']
        y = row['Y']
        pointList.append([x, y])

    # check if points are in polygons and append 0-1 labels to df
    resultsList = []

    for poly in polys:

        label = poly[1]
        path = mpltPath.Path(poly[0])
        single_result = path.contains_points(pointList)
        single_array = np.array(single_result)
        resultsList.append(single_array*label)

    resultsArray = np.array(resultsList)
    final_results = sum([array for array in resultsArray])
    pc['Label'] = final_results

    # removes higher values from overlapping polygons
    pc.loc[pc['Label'] > 1, 'Label'] = 1

    pc = pc.dropna(how='any', axis=0)
    print('output columns: ', pc.columns.values)
    pc.to_csv(output, sep=';', index=False)
    print('done')


if __name__ == '__main__':

    input_file = input('Pointcloud File: ')
    shapes = input("Crater Polygons: ")
    output = input("Output_file: ")
    label_Craters(input_file, shapes, output)