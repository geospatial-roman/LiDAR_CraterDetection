from shapely.geometry import Point, Polygon
import numpy as np
import geopandas

pc_txt = "txt_files/natters_clip_density.txt"
crater_poly = "shapes/krater_manual_Polygons.shp"
output = "txt_files/Clip_Natters_labeled.txt"


shapes = geopandas.read_file(crater_poly)

count = 0
fobj = open(pc_txt, 'r')
fobj_out = open(output, "w")
for line in fobj:

    line = line.strip()
    line = line.split('\t')
    x = float(line[0])
    y = float(line[1])
    z = float(line[2])
    density = float(line[3])
    intensity = float(line[4])
    poi = Point(x, y)

    found = 0
    for index, shape in shapes.iterrows():
        if poi.within(shape['geometry']):
            fobj_out.write("%1.3f\t%1.3f\t%1.3f\t%1.3f\t1\n" % (x, y, z, intensity))
            found = 1
            break
    if found == 0:
        fobj_out.write("%1.3f\t%1.3f\t%1.3f\t%1.3f\t0\n" % (x, y, z, intensity))

    count += 1
    if count % 100000 == 0:
        print(count)

fobj.close()
fobj_out.close()
