import argparse
from pathlib import Path
from typing import List, Optional

import numpy as np

import laspy

from src.bounding_volume import BoundingVolume
from src.tiling.octree_tiling_split import OctreeTilingSplit
from src.tiling.tools import getRange
from src.utils.utils import mkdirIfNotExist

from time import strftime, gmtime


def main():
    # parser = argparse.ArgumentParser(
    #     "LAS recursive splitter", description="Splits a las file bounds recursively"
    # )
    # parser.add_argument("input_file")
    # parser.add_argument("output_dir")
    # parser.add_argument("size", type=tuple_size, help="eg: 50x64.17")
    # parser.add_argument("--points-per-iter", default=10**6, type=int)

    # args = parser.parse_args()
    # print(args)
    input_file = './data/test.las'
    time_stamp = strftime("%Y%m%d%H%M", gmtime())
    output_dir = f"./out/{time_stamp}"
    mkdirIfNotExist(output_dir)
    points_per_iter = 10**6
    max_depth = 4
    # sys.argv[1]

    with laspy.open(input_file) as file:
        header = file.header
        x_min = header.x_min
        x_max = header.x_max
        y_min = header.y_min
        y_max = header.y_max
        z_min = header.z_min
        z_max = header.z_max
        x_offset = header.x_offset
        y_offset = header.y_offset
        z_offset = header.z_offset
        boundingVolume = BoundingVolume(
            x_min, x_max, y_min, y_max, z_min, z_max)

        split = OctreeTilingSplit(max_depth)
        writers: List[Optional[laspy.LasWriter]] = [
            None] * len(split.split_leafs)

        try:
            count = 0
            for points in file.chunk_iterator(points_per_iter):
                print(f"{count / file.header.point_count * 100}%")

                x, y, z = points.x.copy(), points.y.copy(), points.z.copy()
                point_piped = 0
                writersIndex = 0
                for leaf in split.split_leafs:
                    x_coord = leaf.x
                    y_coord = leaf.y
                    z_coord = leaf.z
                    number_of_x = leaf.number_of_x
                    number_of_y = leaf.number_of_y
                    number_of_z = leaf.number_of_z
                    range_x = getRange(x_coord, number_of_x, x_min, x_max)
                    x_min_leaf = range_x[0]
                    x_max_leaf = range_x[1]

                    range_y = getRange(y_coord, number_of_y, y_min, y_max)
                    y_min_leaf = range_y[0]
                    y_max_leaf = range_y[1]

                    range_z = getRange(z_coord, number_of_z, z_min, z_max)
                    z_min_leaf = range_z[0]
                    z_max_leaf = range_z[1]

                    mask = (x >= x_min_leaf) & (x <= x_max_leaf) & (y >= y_min_leaf) & (
                        y <= y_max_leaf) & (z >= z_min_leaf) & (z <= z_max_leaf)

                    if (np.any(mask)):
                        if writers[writersIndex] is None:
                            level_path = output_dir + f"/{max_depth}"
                            mkdirIfNotExist(level_path)
                            output_path = Path(
                                level_path) / f"{x_coord}_{y_coord}_{z_coord}.las"
                            writers[writersIndex] = laspy.open(
                                output_path, mode="w", header=file.header
                            )

                        sub_points = points[mask]
                        writers[writersIndex].write_points(sub_points)

                    point_piped += np.sum(mask)
                    writersIndex += 1
                    if point_piped == len(points):
                        break

                count += len(points)
                print(f"{count / file.header.point_count * 100}%")

        finally:
            for writer in writers:
                if writer is not None:
                    writer.close()


if __name__ == "__main__":
    main()
