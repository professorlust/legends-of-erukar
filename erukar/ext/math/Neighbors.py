class Neighbors:
    def all_adjacent(x, y):
        pass

    def cross_pattern(coord):
        return [
            (coord[0]-1, coord[1]),
            (coord[0]+1, coord[1]),
            (coord[0],   coord[1]-1),
            (coord[0],   coord[1]+1),
        ]

