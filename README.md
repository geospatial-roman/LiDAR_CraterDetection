# PC_Craters


<h2>This Repository contains code to extract Bomb Crater structurs from a LIDAR Laser Scan using Machine Learning and Parameter based Filtering.</h2>

<p>By cloning the repository and running the main file from the corresponding directory. The points in a 3D point cloud, which belong to bomb craters will be classfied and segmented.</p>

<h4>The following parameter can/must be given to run the script</h4>


* -infile     [PATH TO INPUT FILE] (required)
* -outfile    [PATH TO OUTPUT FILE] (required)
* -out_shp    [PATH TO OUTPUT SHP FILE] (required)
* -method     ["Filter", "DecisionTree", "RandomForest"] default="Filter" (optional)
* -clip       [BOOLEAN] default=False (optional)
* -extent     [xmin, ymin, xmax, ymax] (optional)
* -keep_tmp   [BOOLEAN] default=False (optional)



INPUT: File with Point Cloud of Ground point (e.g. use "extract_ground.py" to extract ground points from classified LAS File)
Output: Pointcloud with classified crater points and Shape File with bounding boxes

1. In the prepocessing the LAS File is Filtered for Ground Points and Clipped to the AOI
    (--> preprocessing.extract_ground)
    --> preprocessing.clip_to_aoi

2. Features like Roughness, Curvature, Iluminance are calculated
    --> preprocessing.calculate_params
    
![Alt text](/roughness_3_seite.PNG?raw=true "Optional Title")

3. Pointcloud is filtered for Craters
    --> filtering.filter_params

4. Connected Component Analysis to build segments
    --> utils.region_growing

5. Region growing to extract full crater
    --> utils.region_growing

6. Filtering for unsuitable segments
    --> filtering.filter_segments
    --> filtering.filter_planarity

7. Extraction of final Pointcloud and bounding boxes .shp
    --> utils.bounding_box
    
8. Return Bounding boxes, classified Pointcloud
    
  
