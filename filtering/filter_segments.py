
import pandas as pd
import numpy as np
from utils import check_concavity, calculations


def filter_segments(input):

    """
    :param input_csv: input csv with segmented points for filtern based on size, concavity and linearity
    :return: filtered point cloud df
    """

    if isinstance(input, str):
        input_df = pd.read_csv(input, sep=";")
    else:
        input_df = input

    df2 = pd.DataFrame(input_df['SegmentID'].value_counts())
    df2.reset_index(inplace=True)
    df2.columns = ['SegmentID', 'counts']

    df3 = input_df.merge(df2, on='SegmentID')
    filtered = df3[df3.counts > 120]
    filtered2 = filtered[filtered.counts < 1000]

    appended_data = []
    for seg_id in set(filtered2['SegmentID']):
        df = filtered2[filtered2.SegmentID == seg_id]
        if min(df['X']) == max(df['X']) or min(df['Y']) == max(df['Y']):
            continue

        concave_df = check_concavity.concave(df)
        if min(concave_df['sign']) != 1:
            continue

        df = df.assign(dist=min(concave_df.dist))
        xyzArray = df.filter(items=['X', 'Y', 'Z']).to_numpy()

        covmat, f_mean = calculations.getCovarianceMatrix(xyzArray)
        eL, eI, eS, evecL, evecI, evecS = calculations.getEigenInfos(covmat)

        linearity = (eL - eI) / eL
        vert = 1 - abs(np.dot([0, 0, 1], evecS))

        if linearity < 0.78 and vert < 0.118:
            appended_data.append(df)

    final_df = pd.concat(appended_data)

    return final_df
