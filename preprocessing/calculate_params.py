import os


def cc_cmd_ml(input, output, Xmin=0, Ymin=0, Zmin=0, Xmax=0, Ymax=0, Zmax=0, clip=False):


    command = str('C:\Programme\CloudCompare\CloudCompare -O ')

    command += ' -SKIP 1 '
    command += input
    command += ' -AUTO_SAVE OFF'
    if clip :
        command += ' -CROP %s:%s:%s:%s:%s:%s' % (Xmin, Ymin, Zmin, Xmax, Ymax, Zmax)

    command += ' -DELAUNAY -BEST_FIT -MAX_EDGE_LENGTH 10'
    command += ' -POP_CLOUDS'
    command += ' -CLEAR_CLOUDS'
    command += ' -SAMPLE_MESH DENSITY 10'
    command += ' -POP_MESHES'

    command += ' -CURV GAUSS 3'
    command += ' -ROUGH 3'
    command += ' -CURV MEAN 3'
    command += ' -CURV NORMAL_CHANGE 3'
    command += ' -ROUGH 6'
    command += ' -CURV MEAN 6'
    command += ' -CURV GAUSS 6'
    command += ' -CURV NORMAL_CHANGE 6'
    command += ' -ROUGH 9'
    command += ' -CURV MEAN 9'
    command += ' -CURV GAUSS 9'
    command += ' -CURV NORMAL_CHANGE 9'

    command += ' -PCV -N_RAYS 500 -180 -RESOLUTION 3000'

    command += ' -FEATURE PCA1 3'
    command += ' -FEATURE PCA2 3'
    command += ' -FEATURE SURFACE_VARIATION 3'
    command += ' -FEATURE PCA1 6'
    command += ' -FEATURE PCA2 6'
    command += ' -FEATURE SURFACE_VARIATION 6'
    command += ' -FEATURE PCA1 9'
    command += ' -FEATURE PCA2 9'
    command += ' -FEATURE SURFACE_VARIATION 9'

    command += ' -C_EXPORT_FMT ASC -EXT ".txt"'
    command += ' -SEP SEMICOLON '
    command += ' -ADD_HEADER '
    command += ' -NO_TIMESTAMP'
    command += ' -SAVE_CLOUDS FILE "' + output + '"'

    os.system(command)

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
    command += ' -CURV NORMAL_CHANGE 3'
    command += ' -PCV -N_RAYS 500 -180 -RESOLUTION 3000'

    command += ' -C_EXPORT_FMT ASC -EXT ".txt"'
    command += ' -SEP SEMICOLON '
    command += ' -ADD_HEADER '
    command += ' -NO_TIMESTAMP'
    command += ' -SAVE_CLOUDS FILE "' + output + '"'

    os.system(command)

