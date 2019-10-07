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
    outFile = laspy.file.File(outfile, mode="w", header=inFile.header)
    outFile.points = ground_points
    outFile.close()


def las_to_df(infile, outfile='../tmp/ground.txt', safe=False):


    inFile = laspy.file.File(infile, mode="r")
    dataset = np.vstack(
        [inFile.x, inFile.y, inFile.z, inFile.Intensity, inFile.return_num, inFile.classification]).transpose()

    out_df = pd.DataFrame.from_records(dataset)

    if safe:

        out_df.to_csv(outfile, sep='\t')
    return out_df


