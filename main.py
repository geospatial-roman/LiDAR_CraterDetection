from preprocessing import *
from filtering import *
from utils import *
import datetime
import pickle

import argparse

parser = argparse.ArgumentParser(description="Detect Craters in PointCloud")

parser.add_argument('-infile', required=True,  help='Path to Input File (TXT/LAS)')
parser.add_argument('-outfile', required=True, help='Path to Output Pointcloud (txt)')
parser.add_argument('-out_shp', required=True, help='Path to Output Bounding Boxes (shp)')
parser.add_argument('-method', default="Filter", help='Used Method ["Filter", "DecisionTree", "RandomForest"]')
parser.add_argument('-clip', default=False, help='Clip to extent? (Boolean)')
parser.add_argument('-extent', required=False, help='Extent ("xmin, ymin, xmax, ymax"')
parser.add_argument('-keep_tmp', default=False, help='Save temporary files in folder "tmp" of this directory? (Boolean)')
parser.add_argument('-speed', default="Slow", help='[Fast] will find, but not fill the craters, [Slow] will segment craters up to the edge? ["Slow"."Fast"]')

args = parser.parse_args()


def main(infile, cc_file, final_out, method, clip, crater_shp, xmin=0, ymin=0, xmax=0, ymax=0):

    if method == "Filter":
        """
        if clip:
            cc_cmd_filter(infile, cc_file, xmin, ymin, 0, xmax, ymax, 3000, clip)
        else:
            cc_cmd_filter(infile, cc_file, clip)
        """
        print(str(datetime.datetime.now())[:19], 'Step 1 of 6 - PointCloud clipped to AOI and Attributes calculated')
        filter_df, remaining_df = filter(cc_file)

    elif method == "DecisionTree":

        if clip:
            cc_cmd_ml(infile, cc_file, xmin, ymin, 0, xmax, ymax, 3000, clip)
        else:
            cc_cmd_ml(infile, cc_file, clip)
            df = pd.read_csv(cc_file, sep=";")
            df = df.rename(columns={'//X': 'X'})
            df = df.dropna(how='any', axis=0)
            df_pred = df.drop(['X', 'Y', 'Z', 'Nx', 'Ny', 'Nz'], axis=1)
            print(str(datetime.datetime.now())[:19], 'Step 1 of 6 - PointCloud clipped to AOI and Attributes calculated')

            loaded_model = pickle.load(open('Models/DecisionTreeClassifier.sav', 'rb'))
            prediction = loaded_model.predict(df_pred)

            df['Prediction'] = prediction
            print(str(datetime.datetime.now())[:19], 'Points labeled as craters: ', sum(prediction))
            filter_df = df[df.Prediction == 1]
            remaining_df = df[df.Prediction != 1]

    elif method == "RandomForest":

        if clip:
            cc_cmd_ml(infile, cc_file, xmin, ymin, 0, xmax, ymax, 3000, clip)
        else:
            cc_cmd_ml(infile, cc_file, clip)
            df = pd.read_csv(cc_file, sep=";")
            df = df.rename(columns={'//X': 'X'})
            df = df.dropna(how='any', axis=0)
            df_pred = df.drop(['X', 'Y', 'Z', 'Nx', 'Ny', 'Nz'], axis=1)
            print(str(datetime.datetime.now())[:19], 'Step 1 of 6 - PointCloud clipped to AOI and Attributes calculated')

            loaded_model = pickle.load(open('Models/RandomForestClassifier.sav', 'rb'))
            prediction = loaded_model.predict(df_pred)

            df['Prediction'] = prediction
            print(str(datetime.datetime.now())[:19], 'Points labeld as craters: ', sum(prediction))
            filter_df = df[df.Prediction == 1]
            remaining_df = df[df.Prediction != 1]

    print(str(datetime.datetime.now())[:19], 'Step 2 of 6 - PointCloud classified by ', str(args.method))

    segmented = region_growing(filter_df)
    segmented = segmented.reset_index()
    segmented.to_csv("tmp/segmented.txt", sep=";", index=False)
    print(str(datetime.datetime.now())[:19], 'Step 3 of 6 - PointCloud segmented by Connected Components')


    filtered , remaining_df_2 = filter_segments(segmented)
    print(remaining_df_2)

    remaining_df = pd.concat([remaining_df, remaining_df_2], join="inner", ignore_index=True)
    remaining_df = remaining_df.filter(items=["X", "Y", "Z"])
    filtered.to_csv("tmp/filtered.txt", sep=";", index=False)
    print(str(datetime.datetime.now())[:19], 'Step 4 of 6 - Segments filtered for Craters')

    if args.speed == "Slow":
        print(str(datetime.datetime.now())[:19], "Starting region Growing for crater segmentation. This may take a while.")
        seed_df = find_seeds(filtered, cc_file)
        craters = segment_craters(seed_df, cc_file)
    elif args.speed == "Fast":
        print("Doing it the fast way.")
        craters = filtered

    print(str(datetime.datetime.now())[:19], 'Step 5 of 6 - Craters Classified and Segmented')
    craters = craters.filter(items=["X", "Y", "Z", "SegmentID"])
    craters["Crater"] = 1
    remaining_df["SegmentID"] = 0
    remaining_df["Crater"] = 0

    classified_pc = pd.concat([remaining_df, craters])
    classified_pc.to_csv(final_out, sep=';', index=False)

    bounding_box.draw_bb(craters, crater_shp)
    print(str(datetime.datetime.now())[:19], "Step 6 of 6 - Bounding Box shp created")

    if not args.keep_tmp:
        delete_contents('tmp')


if __name__ == "__main__":

    if args.method not in ["Filter", "DecisionTree", "RandomForest"]:
        print('Please provide a -method argument. Possible methods: ["Filter", "DecisionTree", "RandomForest"]')

    else:
        print(str(datetime.datetime.now())[:19], "Starting with File: ", args.infile)

        tmp_txt = 'tmp/ground_temp.las'
        cc_file = 'tmp/Data_CC_Params.txt'

        if args.clip:
            xmin = args.extent.split()[0]
            ymin = args.extent.split()[1]
            xmax = args.extent.split()[2]
            ymax = args.extent.split()[3]

        main(args.infile, cc_file, args.outfile, args.method, args.clip, args.out_shp, xmin=0, ymin=0, xmax=0, ymax=0)