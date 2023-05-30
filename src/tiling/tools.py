def getRange(coord: int, total: int, min: float, max: float):
    _min = (coord / total) if (total > 0) else 0
    _max = ((coord + 1) / total) if (total > 0) else 1

    _min = min + (max - min) * _min
    _max = min + (max - min) * _max
    return [_min, _max]
