from preprocessing import append_labels


input = 'txt_files/krater_plus1/Data_Lans_filtered.txt'
shapes = 'shapes/kraters_plus1.shp'
output = 'txt_files/krater_plus1/Data_Lans_filtered_plus1.txt'
cat_column = 'None'

append_labels.label_Ones(input,shapes,output)
