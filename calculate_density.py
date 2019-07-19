import numpy as np
from sklearn.neighbors import KDTree

fobj = open("txt_files/Training_clip_Natters.txt", "r")

count = 0
xyzList = []
paramList = []

for line in fobj:
    line = line.strip()
    line = line.split("\t")
    x = float(line[0])
    y = float(line[1])
    z = float(line[2])
    intensity = float(line[3])
    classification = float(line[4])
    xyzList.append([x, y, z])
    paramList.append([intensity, classification])

fobj.close()
xyzArray = np.array(xyzList)
paramArray = np.array(paramList)
print("array created")


# Calculate KDTree and Kernel Density

tree3D = KDTree(xyzArray)
print('tree created')
densityArray = tree3D.kernel_density(xyzArray, h=1)
print("density calculated")

# Write data to new txt file

fobj_out = open("C:/Users/roman/PycharmProjects/PC_Craters/txt_files/natters_clip_density.txt", "w")
for i in range(len(xyzArray)):
    point = xyzArray[i]

    fobj_out.write("%1.3f\t%1.3f\t%1.3f\t%1.3f\t%1.3f\t%1.3f\n" % (point[0], point[1], point[2], densityArray[i], paramArray[i][0], paramArray[i][1]))

fobj_out.close()

print("done")