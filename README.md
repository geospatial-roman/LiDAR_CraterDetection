# CraterDetection

<h2> A tool for automated bomb crater detection in 3D Point Clouds</h2>

<p>This Repository contains code to extract Bomb Crater structurs from a LIDAR Laser Scan using Machine Learning and Parameter based Filtering.</p>

<p>By cloning the repository and running the main file from the corresponding directory. The points in a 3D point cloud, which belong to bomb craters will be classfied and segmented.</p>

<h4>The following parameter can/must be given to run the script</h4>


 **-infile     [PATH TO INPUT FILE]** (required)<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Path to the input Pointcloud in any pointcloud format (.las, .txt, ...)*<br>

 **-outfile    [PATH TO OUTPUT FILE]** (required)<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Path to classified output Pointcloud (will be .txt)*<br>

 **-out_shp    [PATH TO OUTPUT SHP FILE]** (required)<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Path to output .shp file for crater bounding boxes*<br>

 **-method     ["Filter", "DecisionTree", "RandomForest"]** default="Filter" (optional)<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Method to apply: Filter, Decision Tree Classifier or Random Forest Classifier*<br>

 **-clip      [BOOLEAN]** default=False (optional)<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Should the input Pointcloud be clipped?*<br>

 **-extent     [xmin, ymin, xmax, ymax]** (optional)<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*IF Pointcloud should be clipped. This is the extent*<br>

 **-keep_tmp   [BOOLEAN]** default=False (optional)<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*should temporary files be stored or deleted after finishing? Will be in tmp directory*<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*this contains: PointCloud with all calculated Parameters, segments after Classification, Filtered Segments*<br>

 **-speed      ["Slow", "Fast"]** default=Slow (optional)<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Slow: will classify the craters and fill the segments to the whole form.*<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Fast: will identify craters and not fill the segments to the whole form*<br>

Example Usage:


> python main.py -infile ground.las -outfile craters.txt -out_shp craters_bb.shp -method Filter -keep_tmp True -speed Fast


<h3> What does this tool do? </h3>
<p>
Input: File with Point Cloud of Ground point (e.g. use "extract_ground.py" to extract ground points from classified LAS File)</p>
<p>Output: Pointcloud with classified crater points and Shape File with bounding boxes
</p>

1. In the prepocessing the LAS File is Filtered for Ground Points and Clipped to the AOI

2. Features like Roughness, Curvature, Iluminance are calculated
    
![Alt text](/images/roughness_3_seite.PNG?raw=true "Optional Title")

3. Pointcloud is filtered for Craters

4. Connected Component Analysis to build segments

5. Region growing to extract full crater

6. Filtering for unsuitable segments. This filter allows to filter for concave, round, crater-shaped segments. As seen below, by calculating a surface plane, the craters can be distinguished from convex hills and forms.
    
    ![Alt text](/images/plane_in_points.PNG?raw=true "Optional Title")

7. Extraction of final Pointcloud and bounding boxes .shp
    
8. Return Bounding boxes, classified Pointcloud

    ![Alt text](/images/bounding_boxes.jpg?raw=true "Optional Title")
    ![Alt text](/images/filter_example_2.PNG?raw=true "Optional Title")
 
<p> Disclaimer:
The point cloud data, the DTM, and all images and maps are based on data provided by The Amt der Tiroler Landesregierung Abteilung Geoinformation, which is the right full owner of this data.
</p>
