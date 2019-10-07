# PC_Craters
Initial Upload


This Repository contains code to extract Bomb Crater structurs from a LIDAR Laser Scan.

INPUT: Las File of relevant area
Output: Pointcloud reduced to crater points and Shape File with bounding boxes

1. In the prepocessing the LAS File is Filtered for Ground and Clipped to the AOI

2. Features like ROughness, Curvature, Iluminance are calculated

3. Pointcloud is filtered for Craters

4. Connected COmponent Analysis to build segments

5. Region growing to extract full crater

6. Filtering for unsuitable segments

7. Extraction of final Pointcloud and bounding boxes shp
