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

    def direction_between(start, finish):
        angle = Navigator.angle(start, finish)
        return Navigator.angle_to_direction(angle)

    def raytrace(start, finish):
        '''Basic path tracing from one room to another; yields the furthest traversible Room'''
        angle = Navigator.angle(start.coordinates, finish.coordinates)
        hyp = Navigator.distance(start.coordinates, finish.coordinates)
        paths = list(set(Navigator.project(start.coordinates, angle, x) for x in range(math.ceil(hyp)+1)))

        cur = start
        travelled = set({cur.coordinates})
        while True:
            next_room = next((cur.connections[x].room for x in cur.connections \
                              if cur.connections[x].can_see_through() and cur.connections[x].room is not None \
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

    def ccw(A,B,C):
        '''Credit to Bryce Boe ... found at http://bryceboe.com/2006/10/23/line-segment-intersection-algorithm/'''
        return (C[1] - A[1])*(B[0] - A[0]) > (B[1] - A[1])*(C[0] - A[0])

    def intersects(A,B,C,D):
        '''Credit to Bryce Boe ... found at http://bryceboe.com/2006/10/23/line-segment-intersection-algorithm/'''
        return Navigator.ccw(A,C,D) != Navigator.ccw(B,C,D) and Navigator.ccw(A,B,C) != Navigator.ccw(A,B,D)

    def bressenhams(start, finish):
        '''Impl of Bressenham's Line Formula'''
        delta_x = abs(finish[0] - start[0])
        delta_y = abs(finish[1] - start[1])
        delta_err = abs(delta_y | delta_x)
        err = delta_err - 0.5
        x, y = start
        s_x = -1 if start[0] > finish[0] else 1
        s_y = -1 if start[1] > finish[1] else 1
        if delta_x > delta_y:
            err = delta_x / 2.0
            while x != finish[0]:
                yield (x, y)
                err -= delta_y
                if err < 0:
                    y += s_y
                    err += delta_x
                x += s_x
        else: 
            err = delta_y / 2.0
            while y != finish[1]:
                yield (x,y)
                err -= delta_x
                if err < 0:
                    x += s_x
                    err += delta_y
                y += s_y
        yield (x, y)
