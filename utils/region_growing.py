import numpy as np
import pandas as pd
from sklearn.neighbors import KDTree
from math import *
from filtering import filter_planarity


def find_seeds(filtered_in, all_points_in):

    if isinstance(all_points_in, str):
        all_points = pd.read_csv(all_points_in, sep=";")
    else:
        all_points = all_points_in

    if isinstance(filtered_in, str):
        filtered = pd.read_csv(filtered_in, sep=";")
    else:
        filtered = filtered_in

    all_points = all_points.rename(columns={'//X': 'X'})
    filtered = filtered.rename(columns={'//X': 'X'})
    ids = set(filtered['SegmentID'])
    seed_list = []

    for i in ids:
        is_seg = filtered['SegmentID'] == i
        selected = filtered[is_seg]

        xyzArray = all_points.filter(items=['X', 'Y', 'Z']).to_numpy()
        xyArray = all_points.filter(items=['X', 'Y']).to_numpy()

        kdtree = KDTree(xyArray)
        mean_point = [selected['X'].mean(), selected['Y'].mean()]
        idxList = kdtree.query_radius([mean_point], 1)
        nextPoint = xyzArray[idxList[0][0]]

        seed_list.append(nextPoint)

    seed_df = pd.DataFrame.from_records(seed_list)
    return seed_df


def region_growing(input):
    """
    :param input: input csv/txt with
    :return: df with segmented pointcloud
    segments will be built based on distance to nearest point default = 0.6
    """

    if isinstance(input, str):
        input_df = pd.read_csv(input, sep=";")
    else:
        input_df = input

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


    segmented_df = input_df
    segmented_df['SegmentID'] = segmentArray
    segmented_df.loc[segmented_df['SegmentID'] < 0, 'SegmentID'] = 0

    return segmented_df


def segment_craters(mids, all_points):
    """

    :param mids: input middle point of craters
    :param all_points: point cloud continaing total AOI
    :return: df with segmented pointcloud

    segments will be built based on distance to nearest point default = 0.6
    """

    if isinstance(all_points, str):
        input_df = pd.read_csv(all_points, sep=";")
    else:
        input_df = all_points

    if isinstance(mids, str):
        mid_df = pd.read_csv(mids, sep=";")
    else:
        mid_df = mids

    input_df = input_df.rename(columns={'//X': 'X'})
    xyzArray = input_df.filter(items=['X', 'Y', 'Z']).to_numpy()

    tree3D = KDTree(xyzArray)

    ncr_array = input_df['Normal change rate (3)'].to_numpy()
    segmentIds = [-1]*len(xyzArray)
    segmentArray = np.array(segmentIds)

    mid_array = mid_df.to_numpy()

    searchRad = 0.6
    SegID = 0
    for i in range(len(mid_array)):


        MidPt = [mid_array[i]]
        IdxList = tree3D.query_radius(MidPt, searchRad)
        SegID += 1
        Shoots = IdxList[0]
        count = 1
        while len(Shoots) != 0 and count < 2000:
            Seeds = Shoots
            Shoots = []

            for seedID in Seeds:  # aus shoots werden seeds um such zu vergrößern

                segmentArray[seedID] = SegID
                SeedPoint = xyzArray[seedID]  # suche für jeden seed punkt die Nachbarn und appende sie zu Shoots list
                SearchPt = [SeedPoint]
                IdxList = tree3D.query_radius(SearchPt, searchRad)

                for j in range(len(IdxList[0])):

                    idx = IdxList[0][j]
                    dist = sqrt((xyzArray[idx][0]-MidPt[0][0])**2+(xyzArray[idx][1]-MidPt[0][1])**2)
                    if (segmentArray[idx] != -1):
                        continue

                    if ncr_array[idx] > 0.0028 and dist < 7:
                        Shoots.append(idx)
                        segmentArray[idx] = SegID
                        count += 1

    segmented_df = input_df
    segmented_df['SegmentID'] = segmentArray
    segmented_df.loc[segmented_df['SegmentID'] < 0, 'SegmentID'] = 0

    is_seg = segmented_df['SegmentID'] != 0
    segmented_df = segmented_df[is_seg]

    df = filter_planarity.cut_planes(segmented_df)

    return df



