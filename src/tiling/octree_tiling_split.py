from src.tiling.leaf import Leaf


class OctreeTilingSplit:
    def __init__(
            self,
            depth=0,
            number_of_x_in_zero=1,
            number_of_y_in_zero=1,
            number_of_z_in_zero=1):

        self.depth = depth
        self.number_of_x = number_of_x_in_zero * pow(2, depth)
        self.number_of_y = number_of_y_in_zero * pow(2, depth)
        self.number_of_z = number_of_z_in_zero * pow(2, depth)

        self.split_leafs: list[Leaf] = list()

        range_x = range(0, self.number_of_x) if (self.number_of_x > 0) else [0]
        range_y = range(0, self.number_of_y) if (self.number_of_y > 0) else [0]
        range_z = range(0, self.number_of_z) if (self.number_of_z > 0) else [0]

        for x_coord in range_x:
            for y_coord in range_y:
                for z_coord in range_z:
                    leaf = Leaf(self.depth, x_coord, y_coord, z_coord,
                                self.number_of_x, self.number_of_y, self.number_of_z)
                    self.split_leafs.append(leaf)
        
