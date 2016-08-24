from erukar.engine.model.Containable import Containable
from erukar.engine.model.Direction import Direction
from erukar.engine.environment.Passage import Passage
from erukar.engine.environment.Surface import Surface
from erukar.engine.environment.Door import Door
import erukar, random

class Room(Containable):
    def __init__(self, dungeon, coordinates=(0,0)):
        super().__init__([],"","")
        self.dungeon = dungeon
        self.floor = None
        self.ceiling = None
        self.luminosity = 1.0 # luminosity will be used in conjunction with visual skill in descriptions
        self.coordinates = coordinates
        self.connections = {direction: Passage() for direction in Direction}

    def calculate_luminosity(self):
        return self.luminosity

    def calculate_danger(self):
        return 1.0

    def calculate_desirability(self):
        return 1.0

    def connect_room(self, direction, other_room, door=None):
        if other_room is not self:
            self.connections[direction] = Passage(room=other_room, door=door)

    def invert_direction(self, direction):
        return Direction( (direction.value + 2) % 4 )

    def get_in_direction(self, direction):
        return self.connections[direction]

    def coestablish_connection(self, direction, other_room, door=None):
        '''Establishes a connection to both rooms'''
        self.connect_room(direction, other_room, door)
        other_room.connect_room(self.invert_direction(direction), self, door)

    def on_inspect(self, direction):
        '''Not really ever called'''
        return self.description

    def inspect_peek(self, direction, lifeform, scalar=1.0):
        '''A brief peek into the next room; handles aliases of items'''
        aliases = list(self.generate_content_descriptions(lifeform, give_aliases=True, scalar=1.0))
        if len(aliases) > 1:
            aliases[-1] = 'and {}'.format(aliases[-1])
        if len(aliases) > 2:
            return ', '.join(aliases)
        return ' '.join(aliases)

    def add_door(self, direction, door):
        '''Adds a door and sets it up with the next room appropriately'''
        self.connections[direction].door = door
        other_dir = self.invert_direction(direction)
        self.connections[direction].room.connections[other_dir].door = door

    def describe_in_direction(self, direction, lifeform, inspect_walls=False, scalar=1.0):
        '''
        Raytrace. Used to describe a door or set of rooms in a direction from this room.
        inspect_walls is a boolean which allows us to describe the walls we hit with our
        trace (this is False for looking down a set of rooms and in our initial
        descriptions of the room, yet not when looking NESW within our origin room)
        '''
        con = self.connections[direction]
        return con.on_inspect(direction, inspect_walls, lifeform, scalar)

    def describe(self, player):
        '''Used only for the lifeform's current room'''
        room_descriptions = list(self.generate_room_descriptions())
        directions = list(self.generate_direction_descriptions(player.lifeform()))
        contents = list(self.generate_content_descriptions(player.lifeform()))
        return ' '.join(room_descriptions + contents + ['\n'] + directions)

    def visual_description(self):
        lum = self.calculate_luminosity()
        if lum < 0.1:
            return 'The room is completely dark.'
        if lum < 0.3:
            return 'The room is very dimly lit and it is difficult to discern shapes in the darkness.'
        if lum < 0.6:
            return 'The room is dimly lit yet you can still see reasonably well.'
        if lum < 0.9:
            return 'The room is well lit.'
        return 'The room is perfectly bright.'

    def generate_room_descriptions(self):
        yield self.visual_description()  
        if self.floor is not None:
            yield self.floor.on_inspect()
        if self.ceiling is not None:
            yield self.ceiling.on_inspect()

    def content_alias_or_description(self, item, give_alias):
        return item.describe() if not give_alias else item.alias()

    def generate_direction_descriptions(self, lifeform):
        '''Generator for creating a list of directional descriptions'''
        for direction in self.connections:
            res = self.describe_in_direction(direction, lifeform, inspect_walls=False)
            if res is not None:
                yield '\n{0}:\t{1}'.format(direction.name, res)

    def generate_content_descriptions(self, player, give_aliases=False, scalar=1.0):
        '''Generator for creating a list of content descriptions'''
        visible_contents = self.get_visible_contents(player.lifeform(), scalar)
        if len(visible_contents) == 0: 
            yield 'nothing'
        for content in visible_contents:
            if isinstance(content, erukar.engine.lifeforms.Player):
                if content.uid == player.uid:
                    continue
            description = self.content_alias_or_description(content, give_aliases)
            if description is not None:
                yield description

    def directional_inspect(self, direction, lifeform, scalar=1.0):
        '''This is the entry point for looking into other rooms'''
        decay = self.scalar_decay(lifeform.calculate_stat_score('acuity'))
        our_contents = self.inspect_peek(direction, lifeform, scalar)
        if scalar > 0.15:
            their_contents = self.describe_in_direction(direction, lifeform, scalar=scalar*decay)
            return '{}. In the next room, you see {}'.format(our_contents, their_contents)
        return our_contents

    def scalar_decay(self, acuity):
        return 1 / (2 + (20-acuity)/5)

    def adjacent_rooms(self):
        '''Generator which yields rooms we can see into from this one'''
        for c in self.connections:
            passage = self.connections[c]
            if passage.room is not None:
                if passage.door is None or\
                   (isinstance(passage.door, Door) and passage.door.status == Door.Open):
                    yield c

    def walls(self):
        '''Generator for getting only the walls in this room'''
        for direction in self.wall_directions():
            yield self.connections[direction].door

    def wall_directions(self):
        '''Generator for getting the directions which contain only walls'''
        for direction in self.connections:
            passage = self.connections[direction]
            if passage.room is None and isinstance(passage.door, Surface):
                yield direction

    def get_visible_contents(self, lifeform, scalar):
        '''
        The actual acuity score is the flat Acuity score multiplied by the room's
        luminosity coefficient, which ranges from 0.0 (pitch black, very rare) to 1.0
        (absolute brightness.) The scalar value is a value which is used to reduce
        the acu_score further and diminishes at a rate of 0.5 per room.
        '''
        acu_score = lifeform.calculate_stat_score('acuity') * self.calculate_luminosity() * scalar
        return [x for x in self.contents if x.necessary_acuity() <= acu_score]
