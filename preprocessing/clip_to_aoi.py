import numpy as np
import laspy
import os
import pandas as pd

def clip_LAS(infile, outfile, xmin, ymin, xmax, ymax):
    '''
    This function clips a LAS FILE to a Extend and returns a .txt file
    :param infile: Path to LAS file
    :param outfile: Path to new .txt file
    :param xmin: xmin (float)
    :param ymin: ymin (float)
    :param xmax: xmax (float)
    :param ymax: ymax(float)
    :return: txt file with points in aoi
    '''

    inFile = laspy.file.File(infile, mode="r")
    dataset = np.vstack([inFile.x, inFile.y, inFile.z, inFile.Intensity, inFile.return_num, inFile.classification]).transpose()
    print('points full file:', len(dataset))

    count = 0
    clipList= []
    for line in dataset:
        x = line[0]
        y = line[1]

        if xmin < x < xmax and ymin < y < ymax:
            clipList.append(line)
            count += 1



    out_df = pd.DataFrame.from_records(clipList)
    out_df.to_csv(outfile, sep='\t')
    print("done. point sin clip: ", count)




def clip_txt(infile, outfile, xmin, ymin, xmax, ymax):
    '''
        This function clips a LAS FILE to a Extend and returns a .txt file
        :param infile: Path to TXT file
        :param outfile: Path to new .txt file
        :param xmin: xmin (float)
        :param ymin: ymin (float)
        :param xmax: xmax (float)
        :param ymax: ymax(float)
        :return: txt file with points in aoi
        '''
    xyzList = []
    paramList = []
    with open(infile, 'r') as fobj:
        for line in fobj:
            line = line.strip()
            line = line.split('\t')
            x = line[0]
            y = line[1]
            z = line[2]
            if len(line) > 3:
                param_line = [element for element in line[3:]]

            if xmin < x < xmax and ymin < y < ymax:
                xyzList.append([x,y,z])
                paramList.append(param_line)

    fobj.close()

    xyzArray = np.array(xyzList)
    paramArray = np.array(paramList)

    fobj_out = open(outfile, 'w')
    for i in range (len(xyzArray)):
        x = xyzArray[i][0]
        y = xyzArray[i][1]
        z = xyzArray[i][2]
        fobj_out.write('%1.3f\t%1.3f\t%1.3f\t' %(x,y,z) + '%1.3f\t'*(len(paramList)-1) %())


    fobj_out.close()