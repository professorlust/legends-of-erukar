from .Navigator import Navigator
from .Neighbors import Neighbors
import math

import logging
logger = logging.getLogger('debug')

class Distance:
    def direct_traversable(origin, traversable_collection, max_distance):
        visited = []
        pending = [origin]

        while len(pending) > 0:
            examining = pending.pop(0)
            visited.append(examining)
            pending += list(Distance.nearby_direct_traversable(examining, origin, traversable_collection, max_distance, visited))

        return visited

    def nearby_direct_traversable(coord, origin, collection, distance, visited):
        for nbr in Neighbors.cross_pattern(coord):
            if Distance.is_direct_traversable_viable(x, origin, collection, distance, visited):
                yield nbr

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
        possibilities = Neighbors.cross_pattern(coord)
        path_to = paths[coord]
        if len(path_to) > max_path: return []

        for x in possibilities:
            if x not in collection: continue
            if x not in paths or (x in paths and len(paths[x]) < len(path_to)+1):
                cur_path_to = path_to + [x]
                paths[x] = cur_path_to
                yield x

    def direct_los(origin, open_space, max_distance, centered_on=None, radius_around=None):
        if not centered_on: centered_on = origin
        if not radius_around: radius_around = max_distance

        pre_distance_points = [x for x in Distance.points_in_circle(radius_around, centered_on)]
        points = list(sorted(pre_distance_points, key=lambda x: Navigator.distance(origin, x), reverse=True))
        while points:
            line = list(Navigator.bressenhams(origin, points[0]))
            blocker_found = False
            while line:
                coord = line.pop(0)
                if coord in points: points.remove(coord)
                if blocker_found: continue
                if not any(x == coord for x in open_space) or Navigator.distance(coord, origin) > max_distance: 
                    blocker_found = True
                yield coord

    def points_in_circle(radius, origin):
        r = int(radius) 
        for x in range(-r, r+1):
            Y = int((r*r - x*x) ** 0.5)
            for y in range(-Y, Y+1):
                yield (x+origin[0], y+origin[1])
