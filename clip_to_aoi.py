import numpy as np
import laspy
import os


directory = r'C:\Users\roman\Documents\Masterarbeit\relevant_LAS_files'
filename = 'Ground_PC_Mittelgeb_234000_78000.las'


xmin = 80600
xmax = 81050
ymin = 234050
ymax = 234380



inFile = laspy.file.File(os.path.join(directory, str(filename)), mode="r")

#I = inFile.Classification == 2
#inFile.points = inFile.points[I]
dataset = np.vstack([inFile.x, inFile.y, inFile.z, inFile.Intensity, inFile.return_num, inFile.classification]).transpose()

print('points full file:', len(dataset))

count = 0
total_count = 0
fobj_out = open('txt_files/Test_Clip_Lans.txt', 'w')
for line in dataset:
    x = line[0]
    y = line[1]
    z = line[2]

    if xmin < x < xmax and ymin < y < ymax:
        fobj_out.write("%1.3f\t%1.3f\t%1.3f\n" %(line[0], line[1], line[2]))
        count += 1
    total_count +=1
    if total_count % 200000 == 0:
        print(total_count)

print("done. point sin clip: ", count)












'''

xyzList = []
with open(input_txt, 'r') as fobj:
    for line in fobj:
        line = line.strip()
        line = line.split('\t')
        x = line[0]
        y = line[1]
        z = line[2]

        if xmin < x < xmax and ymin < y < ymax:
            xyzList.append([x,y,z])

fobj.close()

xyzArray = np.array(xyzList)

fobj_out = open(str('clip_'+input_txt), 'w')
for line in xyzArray:
    x = line[0]
    y = line[1]
    z = line[2]
    fobj_out.write('%1.3f\t%1.3f\t%1.3f\t' %(x,y,z))


fobj_out.close()
'''