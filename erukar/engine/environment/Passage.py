from erukar.engine.environment.Door import Door
from erukar.engine.environment.Surface import Surface

class Passage:
    def __init__(self, wall=None, room=None, door=None):
        self.door = door
        self.room = room
        self.wall = wall

    def is_door(self):
        return self.door is not None or self.room is not None

    def can_see_or_sense(self, lifeform, depth=0):
        if self.door is None and self.room is not None:
            return True
        acu = lifeform.calculate_effective_stat('acuity', depth)
        return self.door.necessary_acuity() < acu

    def is_not_empty(self):
        return self.door is not None and self.room is not None

    def directional_inspect(self, relative_dir, lifeform, depth=1):
        acu = lifeform.calculate_effective_stat('acuity', depth)
        depth += 1
        if self.door is not None:
            result = self.door.inspect_through(relative_dir, self.room, lifeform, depth)
            if result is not '':
                return '\nRoom {}: {}'.format(depth, result)
            return result
        if self.room is not None:
            result = self.room.directional_inspect(relative_dir, lifeform, depth)
            if result is not '':
                return '\nRoom {}: {}'.format(depth, result)
            return result
        if self.wall is not None:
            return self.wall.describe()
        return ''

    def peek(self, relative_dir, lifeform):
        '''Used when the current room is describing itself'''
        if self.door is not None:
            return self.door.peek(relative_dir, self.room, lifeform)
        if self.room is not None:
            return self.room.describe(lifeform, 1)
        return
