import os


def cc_cmd_ml(input, output):


    os.system(str('C:\Programme\CloudCompare\CloudCompare -O '
                  + ' -GLOBAL_SHIFT AUTO'
                  + ' - SKIP 1 '
                  + input
                  + ' -AUTO_SAVE OFF'
                  #+ ' -CROP %s:%s:%s:%s:%s:%s' % (Xmin, Ymin, Zmin, Xmax, Ymax, Zmax)
                  + ' -DELAUNAY -BEST_FIT -MAX_EDGE_LENGTH 10'
                  + ' -POP_CLOUDS'
                  + ' -CLEAR_CLOUDS'
                  + ' -SAMPLE_MESH DENSITY 10'

                  + ' -CURVE GAUSS 3'
                  + ' -ROUGH 3'
                  + ' -CURV MEAN 3'
                  + ' -CURV NORMAL_CHANGE 3'
                  + ' -ROUGH 6'
                  + ' -CURV MEAN 6'
                  + ' -CURVE GAUSS 6'
                  + ' -CURV NORMAL_CHANGE 6'
                  + ' -ROUGH 9'
                  + ' -CURV MEAN 9'
                  + ' -CURVE GAUSS 9'
                  + ' -CURV NORMAL_CHANGE 9'

                  + ' -PCV -N_RAYS 500 -180 -RESOLUTION 3000'

                  + ' -FEATURE PCA1 3'
                  + ' -FEATURE PCA2 3'
                  + ' -FEATURE SURFACE_VARIATION 3'
                  + ' -FEATURE PCA1 6'
                  + ' -FEATURE PCA2 6'
                  + ' -FEATURE SURFACE_VARIATION 6'
                  + ' -FEATURE PCA1 9'
                  + ' -FEATURE PCA2 9'
                  + ' -FEATURE SURFACE_VARIATION 9'


                  + ' -C_EXPORT_FMT ASC -EXT ".txt"'
                  + ' -SEP SEMICOLON '
                  + ' -ADD_HEADER '
                  + ' -NO_TIMESTAMP'
                  + ' -SAVE_CLOUDS FILE "' + output + '"'))


def cc_cmd_filter(input, output, Xmin=0, Ymin=0, Zmin=0, Xmax=0, Ymax=0, Zmax=0, clip=False):


    command = 'C:\Programme\CloudCompare\CloudCompare -O '
    command += ' -SKIP 1 '
    command += str(input)
    command += ' -AUTO_SAVE OFF'
    if clip:
        command += (' -CROP %s:%s:%s:%s:%s:%s' % (Xmin, Ymin, Zmin, Xmax, Ymax, Zmax))

    command += ' -DELAUNAY -BEST_FIT -MAX_EDGE_LENGTH 10'
    command += ' -POP_CLOUDS'
    command += ' -CLEAR_CLOUDS'
    command += ' -SAMPLE_MESH DENSITY 10'
    command += ' -POP_MESHES'

    command += ' -ROUGH 3'
    command += ' -CURV MEAN 3'
    command += ' -ROUGH 9'
    command += ' -PCV -N_RAYS 500 -180 -RESOLUTION 3000'

    command += ' -C_EXPORT_FMT ASC -EXT ".txt"'
    command += ' -SEP SEMICOLON '
    command += ' -ADD_HEADER '
    command += ' -NO_TIMESTAMP'
    command += ' -SAVE_CLOUDS FILE "' + output + '"'

    os.system(command)

