import numpy as np
import pandas as pd
from sklearn.neighbors import KDTree
from collections import Counter
from utils import calculations, plotting
import itertools

########################################################
# ######          Functions                ########### #
########################################################

def concave(input, plot_plane=False):
    """
    :param input: input csv with segmented points
    :param plot_plane: boolean. if true every crater will be plotted
    :return: dist and sign for each segment, positive: convex, negative: concave
    """

    if isinstance(input, str):
        input_df = pd.read_csv(input, sep=";")
    else:
        input_df = input

    input_df.dropna()

    xyzArray = input_df.filter(items=['X', 'Y', 'Z']).to_numpy()
    xyArray = input_df.filter(items=['X', 'Y']).to_numpy()
    segmentIDs = input_df['SegmentID']
    normalArray = input_df.filter(items=['Nx', 'Ny', 'Nz']).to_numpy()
    kdtree = KDTree(xyArray)

    out_list = []
    sorted_set = set(sorted(segmentIDs, key=Counter(segmentIDs).get, reverse=False))

    for id in sorted_set:
        if id == 0:
            continue

        x = segmentIDs
        get_indexes = lambda x, xs: [i for (y, i) in zip(xs, range(len(xs))) if x == y]
        point_set = get_indexes(id, x)

        if len(point_set) <= 2:
            continue
        xyz_set =[[xyzArray[i][0], xyzArray[i][1], xyzArray[i][2]] for i in point_set]

        X = [x[0] for x in xyz_set]
        Y = [x[1] for x in xyz_set]
        Z = [x[2] for x in xyz_set]

        xmaxx = max(X[0], X[1])
        xsecondmax = min(X[0], X[1])

        for i in range(2, len(X)):
            if X[i] > xmaxx:
                xsecondmax = xmaxx
                xmaxx = X[i]
            else:
                if X[i] > xsecondmax:
                    xsecondmax = X[i]

        yymax = max(Y[0], Y[1])
        ysecondmax = min(Y[0], Y[1])
        for i in range(2, len(Y)):
            if Y[i] > yymax:
                ysecondmax = yymax
                yymax = Y[i]
            else:
                if Y[i] > ysecondmax:
                    ysecondmax = Y[i]

        yymin = min(Y[0], Y[1])
        yysecondmin = max(Y[0], Y[1])
        for i in range(2, len(Y)):
            if Y[i] < yymin:
                yysecondmin = yymin
                yymin = Y[i]
            else:
                if Y[i] < yysecondmin:
                    yysecondmin = Y[i]

        xxmin = max(X[0], X[1])
        xxsecondmin = min(X[0], X[1])

        for i in range(2, len(X)):
            if X[i] < xxmin:
                xxsecondmin = xxmin
                xxmin = X[i]
            else:
                if X[i] < xxsecondmin:
                    xxsecondmin = X[i]

        xmin = np.array(xyz_set[X.index(min(X))])
        ymin = np.array(xyz_set[Y.index(min(Y))])
        xmax = np.array(xyz_set[X.index(max(X))])
        ymax = np.array(xyz_set[Y.index(max(Y))])
        xsecondmax = np.array(xyz_set[X.index(xsecondmax)])
        ysecondmax = np.array(xyz_set[Y.index(ysecondmax)])
        xsecondmin = np.array(xyz_set[X.index(xxsecondmin)])
        ysecondmin = np.array(xyz_set[Y.index(yysecondmin)])

        elem_list = [xmin, ymin, xmax, ymax, xsecondmax, ysecondmax, xsecondmin, ysecondmin]

        for subset in itertools.combinations(elem_list, 3):

            if (subset[0] != subset[1]).all() and (subset[2] != subset[0]).all() and (subset[1] != subset[2]).all():
                break


        mean_point = [float(sum(X) / len(X)), float(sum(Y) / len(Y))]
        dists, idxList = kdtree.query([mean_point], 1)

        nextPoint = xyzArray[idxList[0]]

        dist, sign = calculations.equation_plane_dist(subset[0][0], subset[0][1], subset[0][2], subset[1][0],
                                                      subset[1][1], subset[1][2], subset[2][0],
                                                      subset[2][1], subset[2][2],
                                                      nextPoint[0][0], nextPoint[0][1], nextPoint[0][2])

        if plot_plane:
            plotting.equation_plane_plot(subset[0][0], subset[0][1], subset[0][2], subset[1][0],
                                                          subset[1][1], subset[1][2], subset[2][0],
                                                          subset[2][1], subset[2][2],
                                                          nextPoint[0][0], nextPoint[0][1], nextPoint[0][2], xyzArray)
        out_list.append([nextPoint[0][0], nextPoint[0][1], nextPoint[0][2], sign, dist, id])

    out_df = pd.DataFrame.from_records(out_list, columns=['X', 'Y', 'Z', 'sign', 'dist', 'id'])
    return out_df

