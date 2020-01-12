import preprocessing
import argparse

parser = argparse.ArgumentParser(description="Detect Craters in PointCloud")

parser.add_argument('-infile', required=True,  help='Path to Input File (TXT/LAS)')
parser.add_argument('-outfile', required=True, help='Path to Output Pointcloud (txt)')

args = parser.parse_args()


def main(infile, outfile):
    preprocessing.ground_from_LAS(infile, outfile)


if __name__ == "__main__":

    main(args.infile, args.outfile)