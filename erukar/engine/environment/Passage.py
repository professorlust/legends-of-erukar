from erukar.engine.environment.Door import Door
from erukar.engine.environment.Surface import Surface

class Passage:
    def __init__(self, room=None, door=None):
        self.door = door
        self.room = room

    def is_not_empty(self):
        return self.door is not None and self.room is not None

    def on_inspect(self, relative_dir, inspect_walls, lifeform, scalar=1.0):
        if self.door is not None:
            if isinstance(self.door, Surface) and inspect_walls:
                return self.door.on_inspect(relative_dir.name)
            if type(self.door) is Door:
                return self.describe_door_in_direction(relative_dir, lifeform, scalar)

        if self.room is not None:
            peek = self.room.directional_inspect(relative_dir, lifeform, scalar)
            if len(peek) > 0:
                if scalar == 1.0: # First Room
                    return 'In the first roome, you see {}'.format(peek)
                return peek
            return 'There is nothing inside.'

        return None

    def describe_door_in_direction(self, direction, lifeform, scalar=1.0):
        door_result = self.door.on_inspect(direction)
        if self.door.status == Door.Open:
            door_result += ' ' + self.room.directional_inspect(direction, lifeform, scalar)
        return door_result
