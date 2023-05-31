import numpy as np
import laspy
import open3d as o3d
from pathlib import Path
from time import strftime, gmtime
from laspy import PointFormat, PackedPointRecord
from src.utils.utils import mkdirIfNotExist


def downSample(input_file, output_dir, depth=1, max_depth=1, points_per_iter=2**17):
    output_dir = f"{output_dir}/{depth}"
    mkdirIfNotExist(output_dir)
    output_path = Path(
        output_dir) / f"ds.las"
    with laspy.open(input_file) as file:
        writer = None
        header = file.header
        x_min = header.x_min
        x_max = header.x_max
        y_min = header.y_min
        y_max = header.y_max
        z_min = header.z_min
        z_max = header.z_max
        try:
            count = 0

            for points in file.chunk_iterator(points_per_iter):
                print(f"{count / file.header.point_count * 100}%")
                point_length = len(points)
                mask = [False] * point_length
                offset = 0
                stride = pow(2, max_depth)
                while (offset < point_length + stride):
                    if (depth > 0):
                        range_end = stride if (
                            point_length - offset >= stride) else (point_length - offset)
                        for unit in range(0, range_end):
                            unit_index = unit + offset
                            if (unit >= pow(2, depth - 1) and unit < pow(2, depth)):
                                mask[unit_index] = True
                    else:
                        if (offset < point_length):
                            mask[offset] = True
                    offset += stride

                if (np.any(mask)):
                    if writer is None:

                        writer = laspy.open(
                            output_path, mode="w", header=file.header
                        )
                    sub_points = points[mask]
                    writer.write_points(sub_points)

                count += len(points)
                print(f"{count / file.header.point_count * 100}%")

        finally:
            if writer is not None:
                writer.close()
            return output_path
