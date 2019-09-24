import numpy as np
import pandas as pd
from sklearn.neighbors import KDTree


def region_growing(input):
    """

    :param input: input csv/txt with
    :return: df with segmented pointcloud

    segments will be built based on distance to nearest point default = 0.6
    """

    input_df = pd.read_csv(input, sep=';')
    input_df = input_df.rename(columns={'//X': 'X'})
    xyzArray = input_df.filter(items=['X', 'Y', 'Z']).to_numpy()
    tree3D = KDTree(xyzArray)

    LabelArray = [1]*len(xyzArray)
    segmentIds = [-1]*len(xyzArray)
    segmentArray = np.array(segmentIds)

    searchRad = 0.6
    SegID = 0
    print('Points: ', len(xyzArray))
    for i in range(len(xyzArray)):

        if segmentArray[i] != -1:
            continue
        if (LabelArray[i] != 0):
            SegID += 1
            Shoots = [i]
            count = 1
            while (len(Shoots) != 0):
                Seeds = Shoots
                Shoots = []

                for seedID in Seeds:  # aus shoots werden seeds um such zu vergrößern

                    segmentArray[seedID] = SegID
                    SeedPoint = xyzArray[seedID]  # suche für jeden seed punkt die Nachbarn und appende sie zu Shoots list
                    SearchPt = [SeedPoint]

                    IdxList = tree3D.query_radius(SearchPt, searchRad)

                    for j in range(len(IdxList[0])):

                        idx = IdxList[0][j]
                        if (segmentArray[idx] != -1):
                            continue

                        if LabelArray[idx] != 0:
                            Shoots.append(idx)
                            segmentArray[idx] = SegID
                count += 1

    segmented_df = input_df
    segmented_df['SegmentID'] = segmentArray
    segmented_df.loc[segmented_df['SegmentID'] < 0, 'SegmentID'] = 0

    return segmented_df
