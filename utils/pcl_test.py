
import pcl
import pandas as pd
import pcl.pcl_visualization

import numpy as np

points = pd.read_csv("../tmp/Cloud.txt", sep=" ")
points = points.rename(columns={'//X': 'X'})

xyz = points.filter(items=['X', 'Y', 'Z'])

xyz_array = xyz.to_numpy(dtype='float32')
print(xyz_array)


p = pcl.PointCloud(xyz_array)
print(p)

feat = pcl.DifferenceOfNormalsEstimation(p)

seg = p.make_segmenter_normals(ksearch=200)
seg.set_optimize_coefficients(True)
seg.set_model_type(pcl.SACMODEL_NORMAL_PLANE)
seg.set_normal_distance_weight(0.5)
seg.set_method_type(pcl.SAC_RANSAC)
seg.set_max_iterations(100)
seg.set_distance_threshold(15)
indices, model = seg.segment()

seg_p = p.extract(indices, negative=True)

pcl.save(seg_p, "../tmp/pcl_segs.pcd")
