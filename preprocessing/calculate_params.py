import os


def calculate_params(input, output):

    kernel_size = '3'
    kernel_size_2 = '6'

    os.system(str('C:\Programme\CloudCompare\CloudCompare -O ' + input
                  + ' -AUTO_SAVE OFF'
                  + ' -ROUGH ' + kernel_size
                  + ' -CURV MEAN '+ kernel_size
                  + ' -CURV GAUSS ' + kernel_size
                  + ' -CURV NORMAL_CHANGE ' + kernel_size
                  + ' -ROUGH ' + kernel_size_2
                  + ' -CURV MEAN '+ kernel_size_2
                  + ' -CURV GAUSS ' + kernel_size_2
                  + ' -CURV NORMAL_CHANGE ' + kernel_size_2
                  + ' -C_EXPORT_FMT ASC -EXT ".txt"'
                  + ' -SEP TAB '
                  + ' -ADD_HEADER '
                  + ' -NO_TIMESTAMP'
                  + ' -SAVE_CLOUDS FILE' + output))