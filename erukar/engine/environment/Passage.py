from erukar.engine.environment.Door import Door
from erukar.engine.environment.Surface import Surface

class Passage:
    def __init__(self, room=None, door=None):
        self.door = door
        self.room = room

    def is_door(self):
        return self.door is not None and type(self.door) is Door

    def is_not_empty(self):
        return self.door is not None and self.room is not None

    def directional_inspect_through(self, relative_dir, lifeform, acu, depth=1):
        if self.door is not None:
            return self.door.inspect_through(relative_dir, self.door, lifeform, acu, depth)
        # Otherwise 
        return None

    def peek(self, relative_dir, lifeform):
        '''Used when the current room is describing itself'''
        if self.door is not None:
            if isinstance(self.door, Door):
                return self.door.peek(relative_dir, self.room, lifeform)
        return ''


    def describe_door_in_direction(self, direction, lifeform, continue_after=True, scalar=1.0):
        door_result = self.door.on_inspect(direction)
        if self.door.status == Door.Open and continue_after:
            door_result += ' ' + self.room.directional_inspect(direction, lifeform, scalar)
        return door_result
