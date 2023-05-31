import laspy
from math import floor
from json import dump
from typing import List, Optional
from src.utils.utils import mkdirIfNotExist
from io import TextIOWrapper


def makeIndex(input_file, output_dir,
              max_depth, number_of_x_in_zero=None, number_of_y_in_zero=None,
              number_of_z_in_zero=None):
    mkdirIfNotExist(output_dir)

    writer: Optional[TextIOWrapper] = None
    with laspy.open(input_file) as file:
        try:
            header = file.header
            x_min = header.x_min
            x_max = header.x_max
            y_min = header.y_min
            y_max = header.y_max
            z_min = header.z_min
            z_max = header.z_max

            x_half = x_max - x_min
            y_half = y_max - y_min
            z_half = z_max - z_min

            min_half = min([x_half, y_half, z_half])
            number_of_x_in_zero = number_of_x_in_zero if (
                number_of_x_in_zero is not None) else floor(x_half / min_half)

            number_of_y_in_zero = number_of_y_in_zero if (
                number_of_y_in_zero is not None) else floor(y_half / min_half)

            number_of_z_in_zero = number_of_z_in_zero if (
                number_of_z_in_zero is not None) else floor(z_half / min_half)

            pc_dcr = {
                'max_depth': max_depth,
                'number_of_x_in_zero': number_of_x_in_zero,
                'number_of_y_in_zero': number_of_y_in_zero,
                'number_of_z_in_zero': number_of_z_in_zero,
                'bouding_volume': {
                    'x': x_half * 2,
                    'y': y_half * 2,
                    'z': z_half * 2,
                }
            }
            json_output_dir = f"{output_dir}/index.json"
            writer = open(json_output_dir, 'w')
            dump(pc_dcr, writer, indent=4, ensure_ascii=False)
        finally:
            print('complete write index file !!')
            if (writer is not None):
                writer.close()
            return [number_of_x_in_zero, number_of_y_in_zero, number_of_z_in_zero]
