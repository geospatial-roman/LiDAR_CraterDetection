from osgeo import ogr
import pandas as pd
import numpy as np
import os
from shapely.geometry import Point, MultiPolygon

def draw_bb(input_df, out_shape):
    """
    :param input_csv: input csv with segmented points for filtern based on size, concavity and linearity
    :param out_shape: output .shp file
    :return: filtered point cloud df
    """

    driver = ogr.GetDriverByName('ESRI Shapefile')
    if os.path.exists(out_shape):
        driver.DeleteDataSource(out_shape)
    datasourceOut = driver.CreateDataSource(out_shape)
    layerOut = datasourceOut.CreateLayer('boxes', geom_type=ogr.wkbPolygon25D)
    ID = ogr.FieldDefn('ID', ogr.OFTInteger)
    layerOut.CreateField(ID)
    featureDefn = layerOut.GetLayerDefn()

    count = 0

    for seg_id in set(input_df['SegmentID']):
        df = input_df[input_df.SegmentID == seg_id]

        xmin = df['X'].min()
        xmax = df['X'].max()
        ymin = df['Y'].min()
        ymax = df['Y'].max()
        z = df['Z'].mean()

        featureOut = ogr.Feature(featureDefn)
        outring = ogr.Geometry(ogr.wkbLinearRing)
        outring.AddPoint(xmin, ymin, z)
        outring.AddPoint(xmin, ymax, z)
        outring.AddPoint(xmax, ymax, z)
        outring.AddPoint(xmax, ymin, z)
        outring.AddPoint(xmin, ymin, z)

        polygon = ogr.Geometry(ogr.wkbPolygon)
        polygon.AddGeometry(outring)
        featureOut.SetGeometry(polygon)
        featureOut.SetField('ID', count)
        layerOut.CreateFeature(featureOut)

        count +=1

    featureOut.Destroy()
    datasourceOut.Destroy()
