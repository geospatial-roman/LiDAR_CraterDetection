from shapely.geometry import Point, Polygon
import numpy as np
import geopandas

pc_txt = "txt_files/Training_clip_Natters_xyz.txt"
crater_poly = "shapes/krater_manual_Polygons.shp"
output = "txt_files/Clip_Natters_01.txt"


shapes = geopandas.read_file(crater_poly)

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
        #intensity = float(line[3])
        #returnNum = float(line[4])
        #Classification = float(line[5])
        #roughness = float(line[6])
        #meanCurve = float(line[7])
        #gaussianCurve = float(line[8])
        #normalChange = float(line[9])
        #numNeighbours = float(line[10])
        #Surface_density = float(line[11])
        #Volume_Density = float(line[12])
        #Anistropy = float(line[13])
        #Planarity = float(line[14])
        #Linearity = float(line[15])
        #surface_Variation = float(line[16])
        #sphericity = float(line[17])
        poi = Point(x, y)

        found = 0
        for index, shape in shapes.iterrows():
            if poi.within(shape['geometry']):
                fobj_out.write("%1.3f\t%1.3f\t%1.3f\t1\n" % (x, y, z))\
                    #, roughness, meanCurve, gaussianCurve, normalChange, numNeighbours,
                     #           Anistropy, Planarity, Linearity, surface_Variation, sphericity))
                found = 1
                break
        if found == 0:
            fobj_out.write("%1.3f\t%1.3f\t%1.3f\t0\n" %( x, y, z))

    count += 1
    if count % 100000 == 0:
        print(count)

fobj.close()
fobj_out.close()


#//X Y Z Intensity returnNum Classification Roughness_(12) Mean_curvature_(12) Gaussian_curvature_(12) Normal_change_rate_(12) Number_of_neighbors_(r=12) Surface_density_(r=12) Volume_density_(r=12) Anisotropy_(12) Planarity_(12) Linearity_(12) Surface_variation_(12) Sphericity_(12)