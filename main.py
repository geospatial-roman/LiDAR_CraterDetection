from preprocessing import extract_ground, calculate_params, clip_to_aoi
from filtering import filter_parameters, filter_segments
from utils import region_growing, bounding_box

infile = 'C:/Users/roman/Documents/Masterarbeit/relevant_LAS_files/Ground_PC_Mittelgeb_234000_81000.las'
outfile = 'tmp/ground_temp.las'
tmp_txt = 'txt_files/Master_Raw_Data/High_Density/Data_NO_HighDensity.txt'
cc_file = 'txt_files/costum_filtering/Data_NO_HighDensity_NCR.txt'
final_out = 'txt_files/main_output/234_81_filtered.txt'
crater_shp = 'txt_files/costum_filtering/Data_NO_HighDensity_BoundingBox_120.shp'
ymax = 235600
ymin = 235200
xmax = 82450
xmin = 81600
zmin = 0
zmax = 1000

extract_ground.ground_from_LAS(infile, outfile)
print('ground extracted')
#df = clip_to_aoi.clip_LAS(infile, tmp_txt, xmin, ymin, xmax, ymax)
print('file clipped')

#df.to_csv(tmp_txt, sep=';')
#extract_ground.las_to_df(outfile, tmp_txt, safe=True)
calculate_params.cc_cmd(outfile, xmin, ymin, zmin, xmax, ymax, zmax, cc_file)
print('feature calculated')

filter_df = filter_parameters.filter(cc_file)
print('costum filtered')

segmented = region_growing.region_growing(filter_df)
segmented.to_csv('txt_files/costum_filtering/Data_NO_HighDensity_segmented_120.csv', sep=';', index=False)
print('segmented')

filtered = filter_segments.filter_segments(segmented)
print('segments filtered')

seed_df = region_growing.find_seeds(filtered, cc_file)
print('seeds done')

craters = region_growing.segment_craters(seed_df, cc_file)
craters.to_csv('txt_files/costum_filtering/Data_NO_HighDensity_Craters_120.csv', sep=';', index=False)

bounding_box.draw_bb(craters, crater_shp)


