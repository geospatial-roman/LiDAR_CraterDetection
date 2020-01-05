from preprocessing import append_labels


input = 'txt_files/screenshot_run/Data_Lans_HighDensity_NCR.txt'
shapes = 'shapes/krater_mitte_single.shp'
output = 'txt_files/screenshot_run/Data_Lans_HighDensity_NCR_labeled_2111.txt'

cat_column = 'None'

append_labels.label_Craters(input, shapes, output)
