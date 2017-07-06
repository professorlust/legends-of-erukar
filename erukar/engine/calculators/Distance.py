from erukar.engine.calculators import Navigator
import math

class Distance:
    def direct_traversable(origin, traversable_collection, max_distance):
        visited = []
        pending = [origin]

        while len(pending) > 0:
            examining = pending.pop(0)
            visited.append(examining)
            pending += Distance.nearby_direct_traversable(examining, origin, traversable_collection, max_distance, visited)

        return visited

    def nearby_direct_traversable(coord, origin, collection, distance, visited):
        possibilities = [
            (coord[0]-1, coord[1]),
            (coord[0]+1, coord[1]),
            (coord[0],   coord[1]-1),
            (coord[0],   coord[1]+1),
        ]
        return [x for x in possibilities if Distance.is_direct_traversable_viable(x, origin, collection, distance, visited)]

    def is_direct_traversable_viable(coordinate, origin, collection, distance, visited):
        return any(coordinate == x for x in collection) \
            and not any(coordinate == y for y in visited) \
            and Navigator.distance(coordinate, origin) < distance


    def pathed_traversable(origin, traversable_collection, max_tiles):
        paths = {origin: []}
        pending = [origin]

        while len(pending) > 0:
            examining = pending.pop(0)
            pending += list(Distance.nearby_pathed_traversable(examining, paths, traversable_collection, max_tiles))

        return list(paths.keys())

    def nearby_pathed_traversable(coord, paths, collection, max_path):
        possibilities = [
            (coord[0]-1, coord[1]),
            (coord[0]+1, coord[1]),
            (coord[0],   coord[1]-1),
            (coord[0],   coord[1]+1),
        ]
        path_to = paths[coord]
        if len(path_to) > max_path: return []

        for x in possibilities:
            if x not in collection: continue
            if x not in paths or (x in paths and len(paths[x]) < len(path_to)+1):
                cur_path_to = path_to + [x]
                paths[x] = cur_path_to
                yield x


    def direct_los(origin, open_space, max_distance):
        perimeter = list(set(Distance.points_on_circle_perimeter(max_distance, origin)))
        for perimeter_coord in perimeter:
            for coord in Navigator.bressenhams(origin, perimeter_coord):
                if not any(x == coord for x in open_space): break
                yield coord

    def points_in_circle(radius, origin):
        r = int(radius) 
        for x in range(-r, r+1):
            Y = int((r*r - x*x) ** 0.5)
            for y in range(-Y, Y+1):
                yield(x+origin[0], y+origin[1])

    def points_on_circle_perimeter(radius, origin, num_points=50):
        x, y = origin
        step = 2*math.pi / num_points
        for i in range(0, num_points):
            yield int(x + radius*math.cos(i * step)), int(y + radius*math.sin(i*step) )
