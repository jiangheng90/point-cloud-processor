from time import strftime, gmtime
from json import dump

from src.processor.split import split
from src.processor.down_sample import downSample
from src.processor.make_index import makeIndex


def main():

    # split
    # input_file = './data/test.las'
    # output_dir = "./out"
    # time_stamp = strftime("%Y%m%d%H%M", gmtime())
    # output_dir = f"{output_dir}/{time_stamp}"

    # max_depth = 1
    # split(input_file, output_dir, max_depth)

    # down sample
    input_file = './data/las_Fz_gjz_1003.1.1_Scan_002.xyz_proj.las'
    output_dir = "./out"
    time_stamp = strftime("%Y%m%d%H%M", gmtime())
    output_dir = f"{output_dir}/{time_stamp}"
    max_depth = 2

    division = makeIndex(input_file, output_dir, max_depth)
    for depth in range(0, max_depth + 1):
        ds_file = downSample(input_file, output_dir, depth, max_depth)
        split(ds_file, output_dir, depth, division)


if __name__ == "__main__":
    main()
