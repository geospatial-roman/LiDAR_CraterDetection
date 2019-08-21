import numpy as np
import pandas as pd
from sklearn.neighbors import KDTree
from math import *


########################################################
####             Functions                ##############
########################################################

def getCovarianceMatrix(PointArray):
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


def GetEigenInfos(CovMat):
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


def DistToPlane(Normal,PlanePt,SearchPt):
    Normal /= np.linalg.norm(Normal)
    dist = fabs(np.dot(Normal, PlanePt-SearchPt))
    return dist

def region_growing(input, id_field):

    input_df = pd.read_csv(input, sep='\t')
    xyzArray = input_df.filter(items=['X','Y','Z']).to_numpy()
    tree3D = KDTree(xyzArray)
    LabelArray = np.array(input_df[id_field])
    print(LabelArray)
    segmentIds = [-1]*len(xyzArray)
    segmentArray = np.array(segmentIds)
    #print(segmentIds)
    searchRad = 1.5
    SegID = 0
    print('Points: ', len(xyzArray))
    for i in range(len(xyzArray)):

        if segmentArray[i] != -1:
            continue
        if (LabelArray[i] != 0):
            SegID += 1
            #print(SegID)

            # print("loop over point ", i)
            Shoots = [i]
            count = 1
            while (len(Shoots) != 0):
                Seeds = Shoots
                Shoots = []
                # print(Shoots)
                #print("Shoot: ", count)
                #print("Seeds: ", len(Seeds))
                for seedID in Seeds:  # aus shoots werdem seeds um such zu vergrößern

                    segmentArray[seedID] = SegID
                    SeedPoint = xyzArray[seedID]  # suche für jeden seed punkt die Nachbarn und appende sie zu Shoots list
                    SearchPt = [SeedPoint]

                    IdxList = tree3D.query_radius(SearchPt,searchRad)  # findet alle punkte die in Search Radius um SearchPoint liegen und returned die indizes (liste)
                    #print('idxList: ', len(IdxList))
                    #print(IdxList[0])
                    #if len(IdxList) < 4:
                    #   continue
                    for j in range(len(IdxList[0])):
                        # print(segmentIds[idx])
                        idx = IdxList[0][j]
                        #print('idx:', idx)
                        #print('Label:' ,LabelArray[idx])

                        if (segmentArray[idx] != -1):
                            continue

                        if LabelArray[idx] != 0:
                            Shoots.append(idx)  # punkte die auf der Projezierten Ebene liegen werden der Shoots liste angehänge und in der nächsten iteration als seeds verwendet
                            segmentArray[idx] = SegID
                count += 1
                # print(Shoots)
                # print(Seeds)

        if i % 50000 == 0:
            print(i)

    segmented_df = input_df
    segmented_df['SegmentID'] = segmentArray
    segmented_df.loc[segmented_df['SegmentID'] < 0, 'SegmentID'] = 0
    return segmented_df


def concave(input, output):
    input_df = pd.read_csv(input, sep="\t")
    xyzArray = input_df.filter(items=['X', 'Y', 'Z']).to_numpy()
    segmentIDs = input_df['SegmentID']
    normalArray = input_df.filter(items=['Nx', 'Ny', 'Nz']).to_numpy()

    for id in segmentIDs:
        point_set = []
        for i in range(len(xyzArray)):
            if segmentIDs[i] == id:
                point_set.append(i)

    #xyzSet = np.array[xyzArray[j] for j in point_set]
    CovMat, F_mean = getCovarianceMatrix(point_set)
    eL, eI, eS, evecL , evecI ,evecS = GetEigenInfos(CovMat)

    Normalvector = evecS
    X = [x[0] for x in point_set]
    Y = [x[1] for x in point_set]
    Z = [x[2] for x in point_set]
    mean_point = [X.mean(), Y.mean()]
    kdtree = KDTree(np.dstack((X,Y)).tolist())
    check_point = kdtree.query([mean_point], k=1)
    dist = DistToPlane(Normalvector, plane_Point, check_point)




def tmp_def(input, output):

    input_df = pd.read_csv(input, sep="\t")
    xyzArray = input_df.filter(items=['X', 'Y', 'Z']).to_numpy()
    kdtree = KDTree(xyzArray)

    for i in range(len(xyzArray)):
        point = xyzArray[i]
        dist, pointList = kdtree.query([point], k=5)
        point_set = [xyzArray[j] for j in pointList[0]]
        CovMat, F_mean = getCovarianceMatrix(point_set)
        eL, eI, eS, evecL, evecI, evecS = GetEigenInfos(CovMat)

        print('eL, eI, eS, evecL, evecI, evecS')
        print(eL, eI, eS, evecL, evecI, evecS)
