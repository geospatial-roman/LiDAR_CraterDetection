# PC_Craters
Initial Upload


This Repository contains code to extract Bomb Crater structurs from a LIDAR Laser Scan.

INPUT: Las File or TXT File of relevant area
Output: Pointcloud reduced to crater points and Shape File with bounding boxes

1. In the prepocessing the LAS File is Filtered for Ground Points and Clipped to the AOI \n
    --> preprocessing.extract_ground
    --> preprocessing.clip_to_aoi

2. Features like Roughness, Curvature, Iluminance are calculated
    --> preprocessing.calculate_params

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
    
  
