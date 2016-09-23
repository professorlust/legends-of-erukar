import math, operator

class Navigator:
    '''Static class which does most Pathfinding.'''

    def angle(start, finish):
        '''Calculate the angle (Radians) from 0 to 2*pi between two coordinates'''
        x,y = list(map(operator.sub, finish, start))
        if x == 0:
            return math.pi/2 if y > 0 else 3*math.pi/2
        if y == 0:
            return 0 if x > 0 else math.pi

        angle = math.atan(y/x)
        if x < 0:
            angle += math.pi
        elif y < 0:
            angle += 2*math.pi

        return angle

    def raytrace(start, finish):
        '''Basic path tracing from one room to another; yields the furthest traversible Room'''
        angle = Navigator.angle(start.coordinates, finish.coordinates)
        hyp = Navigator.distance(start.coordinates, finish.coordinates)
        paths = list(set(Navigator.project(start.coordinates, angle, x) for x in range(math.ceil(hyp)+1)))

        cur = start
        travelled = set({cur.coordinates})
        while True:
            next_room = next((cur.connections[x].room for x in cur.connections \
                              if cur.connections[x].can_see_through() \
                              and cur.connections[x].room.coordinates not in travelled\
                              and cur.connections[x].room.coordinates in paths), None)
            if next_room is None or cur is finish:
                return cur
            travelled.add(next_room.coordinates)
            cur = next_room

    def project(start, angle, magnitude):
        '''project an angle from the start coordinates and a magnitude'''
        return int(start[0] + magnitude*math.cos(angle)), int(start[1] + magnitude*math.sin(angle))

    def distance(start, finish):
        return math.sqrt(sum(math.pow(a-b, 2) for a,b in zip(finish, start)))

    def exists_obstruction_between(start, finish):
        raytrace_collision = Navigator.raytrace(start, finish)
        return raytrace_collision != finish
