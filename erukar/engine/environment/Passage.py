from erukar.engine.environment.Door import Door
from erukar.engine.environment.Surface import Surface
from erukar.engine.model.RpgEntity import RpgEntity 

class Passage(RpgEntity):
    def __init__(self, wall=None, rooms=None, door=None):
        super().__init__()
        self.door = door
        self.rooms = [] if not rooms else rooms 
        self.wall = wall
        self.coordinates = (0,0)

    def add_room(self, room):
        if len(self.rooms) > 1:
            raise Exception('Already at maximum capacity for rooms in passage {}'.format(self))
        self.rooms.append(room)

    def is_valid(self):
        return len(self.rooms) == 2

    def can_traverse_through(self):
        return (self.door is not None and self.door.status is Door.Open) or (self.door is None and len(self.rooms) == 2)

    def has_door(self):
        return self.door is not None

    def can_detect(self, lifeform, efficiency=1.0):
        if not self.has_door():
            return self.is_valid()
        acu = lifeform.calculate_effective_stat('acuity') * efficiency
        return self.door.necessary_acuity() < acu

    def next_room(self, from_room):
        return next(x for x in self.rooms if x is not from_room)

    def next_visible(self, from_room):
        if self.has_door() and self.door.status is not Door.Open:
            return self.door
        return self.next_room(from_room)

    def directional_inspect(self, relative_dir, lifeform, depth=1):
        return 'Directional inspection is undergoing a rework'

    def peek(self, lifeform, acu, sen):
        '''Used when the current room is describing itself'''
        return self.next_visible(lifeform.room).peek(lifeform, acu, sen)

    def on_open(self, player):
        if self.has_door():
            return self.door.on_open(player)

    def on_close(self, player):
        if self.has_door():
            return self.door.on_close(player)

    def describe(self, from_room):
        return 'Connection'
