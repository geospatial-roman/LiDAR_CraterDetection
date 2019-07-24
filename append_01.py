from shapely.geometry import Point, Polygon
import numpy as np
import geopandas
import matplotlib.path as mpltPath
import datetime

pc_txt = "txt_files/HighDensity_Data_Natters.txt"
crater_poly = "shapes/krater_manual_Polygons.shp"
output = "txt_files/HighDensity_Data_Natters_Labeled_matplot.txt"


print(datetime.datetime.now(), 'Starting with File: ', pc_txt)
shapes = geopandas.read_file(crater_poly)
pointList = []
paramList = []
xyzList = []

g = [i for i in shapes.geometry]

polys = []
for i in range(len(g)):

    x,y = g[i].exterior.coords.xy
    coords = np.dstack((x,y)).tolist()
    polys.append(coords)





count = 0
fobj = open(pc_txt, 'r')
fobj_out = open(output, "w")
for line in fobj:
    if count > 0:
        line = line.strip()
        line = line.split('\t')
        x = float(line[0])
        y = float(line[1])
        z = float(line[2])
        roughness_12 = float(line[3])
        Meancurvature_12 = float(line[4])
        Gaussiancurvature_12 = float(line[5])
        Normalchange_12 = float(line[6])
        Planarity_12 = float(line[7])
        Linearity_12 = float(line[8])
        Surfacevariation_12 = float(line[8])
        Sphericity_12 = float(line[10])
        Roughness_6 = float(line[11])
        Meancurvature_6 = float(line[12])
        Gaussiancurvature_6 = float(line[13])
        Normalchange_6 = float(line[14])
        Planarity_6 = float(line[15])
        Linearity_6 = float(line[16])
        Surfacevariation_6 = float(line[17])
        Sphericity_6 = float(line[18])
        Roughness_3 = float(line[19])
        Meancurvature_3 = float(line[20])
        Gaussiancurvature_3 = float(line[21])
        Normalchange_3 = float(line[22])
        Planarity_3 = float(line[23])
        Linearity_3 = float(line[24])
        Surfacevariation_3 = float(line[25])
        Sphericity_3 = float(line[26])
        Nx = float(line[27])
        Ny = float(line[28])
        Nz = float(line[29])
        pointList.append([x,y])
        xyzList.append([x,y,z])
        paramList.append([roughness_12, Meancurvature_12, Gaussiancurvature_12, Normalchange_12, Planarity_12, Linearity_12, Surfacevariation_12,
                                  Sphericity_12, Roughness_6, Meancurvature_6, Gaussiancurvature_6, Normalchange_6, Planarity_6, Linearity_6, Surfacevariation_6,
                                  Sphericity_6, Roughness_3, Meancurvature_3, Gaussiancurvature_3, Normalchange_3, Planarity_3, Linearity_3, Surfacevariation_3, Sphericity_3,
                                  Nx, Ny, Nz])


    count += 1
    if count % 1000000 == 0:
        print(count)


fobj.close()
paramArray = np.array(paramList)
xyzArray = np.array(xyzList)
resultsList = []
print(datetime.datetime.now(), 'pointList: ', len(pointList))
print(datetime.datetime.now(),  'arrays created')
for poly in polys:

    path = mpltPath.Path(poly[0])
    single_result = path.contains_points(pointList)
    resultsList.append(single_result)

resultsArray = np.array(resultsList)
final_results = sum([array for array in resultsArray])

print(datetime.datetime.now(), final_results)
print(datetime.datetime.now(), sum(final_results), 'point sin craters')



for i in range(len(xyzArray)):
    fobj_out.write("%1.3f\t%1.3f\t%1.3f\t%1.3f\t%1.3f\t%1.3f\t%1.3f\t%1.3f\t%1.3f\t%1.3f\t%1.3f\t%1.3f\t%1.3f\t%1.3f\t%1.3f\t%1.3f\t%1.3f\t%1.3f\t%1.3f\t"
                       "%1.3f\t%1.3f\t%1.3f\t%1.3f\t%1.3f\t%1.3f\t%1.3f\t%1.3f\t%1.3f\n"
                       % (xyzArray[i][0], xyzArray[i][1], xyzArray[i][2],final_results[i], paramArray[i][0], paramArray[i][1], paramArray[i][2], paramArray[i][3], paramArray[i][4],
                          paramArray[i][5],
                          paramArray[i][7], paramArray[i][8], paramArray[i][9], paramArray[i][10], paramArray[i][11], paramArray[i][12], paramArray[i][13],
                          paramArray[i][15], paramArray[i][16], paramArray[i][17], paramArray[i][18], paramArray[i][19], paramArray[i][20], paramArray[i][21],
                          paramArray[i][23],paramArray[i][24], paramArray[i][25], paramArray[i][26]))



fobj_out.close()
print(datetime.datetime.now(), 'done')

