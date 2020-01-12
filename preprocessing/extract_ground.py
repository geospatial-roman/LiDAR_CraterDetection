import numpy as np
import laspy
import pandas as pd

def ground_from_LAS(infile, outfile):
    '''
    This function clips a LAS FILE to a Extend and returns a .txt file
    :param infile: Path to LAS file
    :param outfile: Path to new .txt file
    :return: txt file with points in aoi
    '''

    inFile = laspy.file.File(infile, mode="r")

    ground_points = inFile.points[inFile.classification == 2]
    #dataset = np.vstack(
        #[ground_points.x, ground_points.y, ground_points.z, ground_points.Intensity, ground_points.return_num, ground_points.classification]).transpose()

    """
    count = 0
    clipList = []
    for line in dataset:
        x = line[0]
        y = line[1]
        z = line[2]

        if xmin < x < xmax and ymin < y < ymax:
            clipList.append([x, y, z])
            count += 1

    out_df = pd.DataFrame.from_records(dataset)
    """
    outFile = laspy.file.File(outfile, mode="w", header=inFile.header)
    outFile.points = ground_points
    outFile.close()

    #return out_df


def las_to_df(infile, outfile='../tmp/ground.txt', safe=False):


    inFile = laspy.file.File(infile, mode="r")
    dataset = np.vstack(
        [inFile.x, inFile.y, inFile.z, inFile.Intensity, inFile.return_num, inFile.classification]).transpose()

    out_df = pd.DataFrame.from_records(dataset)

    if safe:

        out_df.to_csv(outfile, sep='\t')
    return out_df


