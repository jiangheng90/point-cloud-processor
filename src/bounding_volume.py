class HalfAxis:
    def __init__(self):
        self.min = 0
        self.max = 0
        self.length = 0
        

class BoundingVolume:
    def __init__(self, x_min, x_max, y_min, y_max, z_min, z_max):
        self.x = HalfAxis()
        self.x.min = x_min
        self.x.max = x_max
        self.x.length = x_max - x_min

        self.y = HalfAxis()
        self.y.min = y_min
        self.y.max = y_max
        self.y.length = y_max - y_min

        self.z = HalfAxis()
        self.z.min = z_min
        self.z.max = z_max
        self.z.length = z_max - z_min