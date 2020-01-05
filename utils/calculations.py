
import numpy as np
from math import *


def getCovarianceMatrix(PointArray):
    """
    :param PointArray: input Point Cloud
    :return: Covariance Matrix , F_Mean
    """
    F_mean = np.mean(PointArray, axis=0)
    CovMat = np.matrix([[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]])
    for P in PointArray:
        CovMat[0, 0] += ((P[0] - F_mean[0]) ** 2)
        CovMat[0, 1] += (P[0] - F_mean[0]) * (P[1] - F_mean[1])
        CovMat[0, 2] += (P[0] - F_mean[0]) * (P[2] - F_mean[2])

        CovMat[1, 0] += (P[0] - F_mean[0]) * (P[1] - F_mean[1])
        CovMat[1, 1] += ((P[1] - F_mean[1]) ** 2)
        CovMat[1, 2] += (P[1] - F_mean[1]) * (P[2] - F_mean[2])

        CovMat[2, 0] += (P[0] - F_mean[0]) * (P[2] - F_mean[2])
        CovMat[2, 1] += (P[1] - F_mean[1]) * (P[2] - F_mean[2])
        CovMat[2, 2] += ((P[2] - F_mean[2]) ** 2)
    return CovMat, F_mean


def getEigenInfos(CovMat):
    """
    :param CovMat: Input Covariance Matrix
    :return: Eigenwert_L, Eigenwert_I, Eigenwert_S, Eigenvektor_L, Eigenvektor_I, Eigenvektor_S
    """
    # get eigenvalues and eigenvectors
    eigenvalues_unsorted, eigenvectors_unsorted = np.linalg.eig(CovMat)

    # sort eigenvalues and eigenvectors
    idx = eigenvalues_unsorted.argsort()[::-1]
    eigenvalues = eigenvalues_unsorted[idx]
    eigenvectors = eigenvectors_unsorted[:, idx]

    # write out and reformat values
    eL = eigenvalues[0]
    eI = eigenvalues[1]
    eS = eigenvalues[2]
    evecL = np.array(eigenvectors[:, 0].T)
    evecI = np.array(eigenvectors[:, 1].T)
    evecS = np.array(eigenvectors[:, 2].T)

    return eL / eL, eI / eL, eS / eL, evecL[0], evecI[0], evecS[0]



def equation_plane_dist(x1, y1, z1, x2, y2, z2, x3, y3, z3, x4, y4, z4):
    """

    :param x1: X Coordinate Plane point 1
    :param y1: Y Coordinate Plane point 1
    :param z1: Z Coordinate Plane point 1
    :param x2: X Coordinate Plane point 2
    :param y2: Y Coordinate Plane point 2
    :param z2: Z Coordinate Plane point 2
    :param x3: X Coordinate Plane point 3
    :param y3: Y Coordinate Plane point 3
    :param z3: Z Coordinate Plane point 3
    :param x4: X Coordinate point of Interest
    :param y4: Y Coordinate point of Interest
    :param z4: Z Coordinate point of Interest
    :return: Distance to plane , Sign
    """

    a1 = x2 - x1
    b1 = y2 - y1
    c1 = z2 - z1
    a2 = x3 - x1
    b2 = y3 - y1
    c2 = z3 - z1
    a = b1 * c2 - b2 * c1
    b = a2 * c1 - a1 * c2
    c = a1 * b2 - b1 * a2
    d = (- a * x1 - b * y1 - c * z1)

    z = (1 / c) * (a * x1 + b * y1 + c * z1 - a * x4 - b * y4)

    if z > z4:
        sign = 1

    else:
        sign = -1

    dist = z - z4

    return dist, sign




