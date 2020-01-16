import utils
import pandas as pd
import numpy as np
import datetime



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
    print(str(datetime.datetime.now())[:19], "Segments: ", len(set(filtered2['SegmentID'])))
    appended_data = []
    remaining_data = []
    for seg_id in set(filtered2['SegmentID']):
        df = filtered2[filtered2.SegmentID == seg_id]
        if min(df['X']) == max(df['X']) or min(df['Y']) == max(df['Y']):
            continue

        concave_df = utils.concave(df)
        if min(concave_df['sign']) != 1:
            remaining_data.append(concave_df)
            continue

        df = df.assign(dist=min(concave_df.dist))
        xyzArray = df.filter(items=['X', 'Y', 'Z']).to_numpy()

        covmat, f_mean = utils.getCovarianceMatrix(xyzArray)
        eL, eI, eS, evecL, evecI, evecS = utils.getEigenInfos(covmat)

        linearity = (eL - eI) / eL
        vert = 1 - abs(np.dot([0, 0, 1], evecS))

        if linearity < 0.78 and vert < 0.118:
            appended_data.append(df)

    final_df = pd.concat(appended_data)
    remaining_df = pd.concat(remaining_data)
    print(str(datetime.datetime.now())[:19], "Craters: ", len(set(final_df['SegmentID'])))

    return final_df, remaining_df


def filter_segments_ml(input):

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
    filtered = df3[df3.counts > 20]
    filtered2 = filtered[filtered.counts < 1000]

    appended_data = []
    for seg_id in set(filtered2['SegmentID']):
        df = filtered2[filtered2.SegmentID == seg_id]
        if min(df['X']) == max(df['X']) or min(df['Y']) == max(df['Y']):
            continue

        concave_df = utils.concave(df)
        if min(concave_df['sign']) != 1:
            continue

        df = df.assign(dist=min(concave_df.dist))
        xyzArray = df.filter(items=['X', 'Y', 'Z']).to_numpy()

        covmat, f_mean = utils.getCovarianceMatrix(xyzArray)
        eL, eI, eS, evecL, evecI, evecS = utils.getEigenInfos(covmat)

        linearity = (eL - eI) / eL
        vert = 1 - abs(np.dot([0, 0, 1], evecS))

        if linearity < 0.78 and vert < 0.118:
            appended_data.append(df)

    final_df = pd.concat(appended_data)

    return final_df



if __name__ == '__main__':
    print("This Module should not be used stand alone. it is based on DataFrames")
