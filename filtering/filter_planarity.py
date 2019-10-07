import numpy as np
import pandas as pd
from sklearn.neighbors import KDTree
from utils import calculations



def cut_planes(input_df):
    """
    :param input_csv: input csv with segmented points for filtern based on size, concavity and linearity
    :return: filtered point cloud df
    """

    appended_data = []

    for seg_id in set(input_df['SegmentID']):
        df = input_df[input_df.SegmentID == seg_id]

        xyzArray = df.filter(items=['X', 'Y', 'Z']).to_numpy()
        tree3D = KDTree(xyzArray)
        plane_array = [0]*len(xyzArray)

        for i in range(len(xyzArray)):
            SearchPt = [xyzArray[i]]
            IdxList = tree3D.query_radius(SearchPt, 3)

            pointSet = [xyzArray[j] for j in IdxList[0]]

            CovMat, F_mean = calculations.getCovarianceMatrix(pointSet)
            eL, eI, eS, evecL, evecI, evecS = calculations.getEigenInfos(CovMat)

            planarity = (eI-eS)/eL
            plane_array[i] = planarity

        df = pd.DataFrame(df)
        df['Planarity'] = np.array(plane_array)
        is_seg = df['Planarity'] > 0.5
        segmented_df = df[is_seg]

        if len(segmented_df.index) > 250:
            appended_data.append(segmented_df)

    final_df = pd.concat(appended_data)

    return final_df

