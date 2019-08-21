import numpy as np
import pandas as pd


def filter_points(input, field='Gaussian curvature (3)',threshold=0.001):
    '''
    :param input: pointcloud .txt
    :param output: pointcloud .txt
    :param threshold: default: 0.001
    :return:
    '''

    input_df = pd.read_csv(input, sep='\t')
    is_relevant = input_df[field] > threshold
    filtered = input_df[is_relevant]

    return filtered