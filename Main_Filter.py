from preprocessing import *
from filtering import *
from utils import *
import datetime


if __name__ == '__main__':


    print("starting Main Filter Script")
    infile = 'C:/Users/roman/Documents/Masterarbeit/relevant_LAS_files/Ground_PC_Mittelgeb_234000_81000.las'
    outfile = 'tmp/ground_temp.las'
    tmp_txt = 'tmp/ground_temp.las'
    cc_file = 'tmp/Data_Lans_HighDensity_Params.txt'
    final_out = 'txt_files/2020_checks/FILTER_MAIN_TEST.txt'
    crater_shp = 'txt_files/2020_checks/FILTER_MAIN_TEST_BB.shp'
    inputformat = "TXT"

    ymax = 235761
    ymin = 234334
    xmin = 79332
    xmax = 82958
    zmin = 0
    zmax = 1500

    print(str(datetime.datetime.now())[:19], ' Starting file: ', infile)


    if inputformat == "LAS":

        #extract_ground.
        #ground_from_LAS(infile, outfile)
        #clip_LAS(infile, outfile, xmin, ymin, xmax, ymax)
        print(str(datetime.datetime.now())[:19],'File clipped to AOI and Ground Points extracted')

        #df.to_csv(tmp_txt, sep=';')
        las_to_df(outfile, tmp_txt, safe=False)
        cc_cmd_filter(tmp_txt, cc_file)
        print(str(datetime.datetime.now())[:19],'Features calculated')

    else:
        tmp_txt = infile
        cc_cmd_filter(tmp_txt, cc_file, xmin, ymin, zmin, xmax, ymax, zmax, clip=True)
        print(str(datetime.datetime.now())[:19], 'features calculated')

    filter_df = filter(cc_file)
    print(str(datetime.datetime.now())[:19], 'PointCloud filtered by Attributes')

    segmented = region_growing(filter_df)
    #segmented.to_csv('txt_files/screenshot_run/Lans_screenshots_cc_segmented.txt', sep=';', index=False)
    print(str(datetime.datetime.now())[:19], 'PointCloud segmented by Connected Components')

    #segmented = pd.read_csv('txt_files/screenshot_run/Lans_screenshots_cc_segmented.txt', sep=';')
    filtered = filter_segments(segmented)
    print(str(datetime.datetime.now())[:19], 'Segments filtered for Craters')
    
    seed_df = find_seeds(filtered, cc_file)
    print("Seeds created")
    craters = segment_craters(seed_df, cc_file)
    #craters.to_csv('txt_files/screenshot_run/Lans_screenshots_final.txt', sep=';', index=False)
    print(str(datetime.datetime.now())[:19], 'Craters Classified and Segmented')
    
    bounding_box.draw_bb(craters, crater_shp)
    print(str(datetime.datetime.now())[:19], "Bounding Box shp created")
    
    delete_contents('tmp')