import os


def cc_cmd(input, Xmin, Ymin, Zmin, Xmax, Ymax, Zmax, output):

    kernel_size_1 = '3'
    kernel_size_2 = '9'

    os.system(str('C:\Programme\CloudCompare\CloudCompare -O ' + input
                  + ' -AUTO_SAVE OFF'
                  + ' -CROP %s:%s:%s:%s:%s:%s' % (Xmin, Ymin, Zmin, Xmax, Ymax, Zmax)
                  + ' -DELAUNAY -BEST_FIT -MAX_EDGE_LENGTH 10'
                  + ' -POP_CLOUDS'
                  + ' -CLEAR_CLOUDS'
                  + ' -SAMPLE_MESH DENSITY 10'
                  + ' -ROUGH ' + kernel_size_1
                  + ' -CURV MEAN ' + kernel_size_1
                  + ' -ROUGH ' + kernel_size_2
                  + ' -CURV NORMAL_CHANGE ' + kernel_size_1
                  + ' -PCV -N_RAYS 500 -180 -RESOLUTION 3000'
                  + ' -C_EXPORT_FMT ASC -EXT ".txt"'
                  + ' -SEP SEMICOLON '
                  + ' -ADD_HEADER '
                  + ' -NO_TIMESTAMP'
                  + ' -SAVE_CLOUDS FILE "' + output + '"'))

