
import pandas as pd
from preprocessing import *
from utils import *
from filtering import *

infile = 'C:/Users/roman/Documents/Masterarbeit/relevant_LAS_files/Ground_PC_Mittelgeb_234000_81000.las'
outfile = 'tmp/ground_temp.las'
tmp_txt = 'txt_files/Master_Raw_Data/High_Density/Data_Natters_HighDensity.txt'
cc_file = 'txt_files/screenshot_run/Data_Lans_HighDensity_NCR.txt'
final_out = 'txt_files/screenshot_run/Lans_screenshots.txt'
crater_shp = 'txt_files/screenshot_run/Data_Lans_HighDensity_BoundingBox_120.shp'

ymax = 233200
ymin = 231500
xmax = 39500
xmin = 38200

zmin = 0
zmax = 1500

39485
# Lans
# ymax = 235600
# ymin = 235200
# xmax = 82450
# xmin = 81600
# zmin = 0
# zmax = 1000

#Natters
# ymax = 233200
# ymin = 231500
# xmax = 39500
# xmin = 38200
# zmin = 0
# zmax = 1500


#extract_ground.
ground_from_LAS(infile, outfile)
print('ground extracted')
df = clip_LAS(infile, tmp_txt, xmin, ymin, xmax, ymax)
print('file clipped')

df.to_csv(tmp_txt, sep=';')
las_to_df(outfile, tmp_txt, safe=False)
# xmin, ymin, zmin, xmax, ymax, zmax
cc_cmd_filter(tmp_txt, cc_file)
print('feature calculated')


filter_df = filter(cc_file)
print('costum filtered')
filter_df.to_csv('txt_files/screenshot_run/Lans_screenshots_cc_filter_2111.txt', sep=";", index=False)


segmented = region_growing(filter_df)
segmented.to_csv('txt_files/screenshot_run/Lans_screenshots_cc_segmented.txt', sep=';', index=False)
print('segmented')
segmented = pd.read_csv('txt_files/costum_filtering/Data_Lans_HighDensity_segmented_120.csv', sep=';')

filtered = filter_segments(segmented)
filtered.to_csv('txt_files/screenshot_run/Lans_screenshots_cc_filtered.txt', sep=';', index=False)
print('segments filtered')

seed_df = find_seeds(filtered, cc_file)
print('seeds done')

craters = segment_craters(seed_df, cc_file)
craters.to_csv('txt_files/screenshot_run/Lans_screenshots_final.txt', sep=';', index=False)

bounding_box.draw_bb(craters, crater_shp)

