import numpy as np
import laspy
import pandas as pd


def clip_LAS(infile, outfile, xmin, ymin, xmax, ymax, safe=False):
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
    dataset = np.vstack([inFile.x,
                         inFile.y,
                         inFile.z
                         ]).transpose()
    print('dataset created')
    df = pd.DataFrame.from_records(dataset, columns=['X', 'Y', 'Z'])
    print('dataset now df')
    print(len(df.index()))

    is_seg = xmin < df['X'] < xmax
    df = df[is_seg]

    is_seg = ymin < df['Y'] < ymax
    df = df[is_seg]

    #df_aoi = df[(xmax > df['X'] > xmin) & (ymax > df['Y'] > ymin)]

    """
    count = 0
    clipList= []
    for line in dataset:
        x = line[0]
        y = line[1]
        z = line[2]

        if xmin < x < xmax and ymin < y < ymax:
            clipList.append([x, y, z])
            count += 1


    outFile = laspy.file.File(outfile, mode="w", header=inFile.header)
    outFile.points = clipList
    outFile.close()
    """

    if safe:

        df.to_csv(outfile, sep='\t')
    return df




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