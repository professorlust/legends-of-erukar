from erukar.engine.model.Containable import Containable
from erukar.engine.model.Direction import Direction
from erukar.engine.environment.Passage import Passage
from erukar.engine.environment.Surface import Surface
from erukar.engine.environment.Door import Door
from erukar.engine.environment.Decoration import Decoration
import erukar, random

class Room(Containable):
    def __init__(self, dungeon, coordinates=(0,0)):
        super().__init__([])
        self.dungeon = dungeon
        if self.dungeon is not None:
            self.dungeon.rooms.append(self)
        self.floor = None
        self.ceiling = None
        self.coordinates = coordinates
        self.connections = {direction: Passage() for direction in Direction}
        self.visible_in_room_description = False

    def calculate_luminosity(self):
        luminosity = 0
        for x in self.dungeon.get_applicable_auras(self):
            if hasattr(x, 'modify_light'):
                luminosity += x.modify_light()
        return min(1.0, luminosity)

    def calculate_danger(self):
        return 1.0

    def calculate_desirability(self):
        return 1.0

    def initiate_aura(self, aura):
        aura.location = self
        self.dungeon.active_auras.add(aura)

    def directional_inspect(self, direction, lifeform, depth=0):
        '''e.g. INSPECT NORTH'''
        connection_result = self.connections[direction].directional_inspect(direction, lifeform, depth)
        acu = lifeform.calculate_effective_stat('acuity', depth)
        if depth == 0:
            return connection_result
        if acu < 1 and depth > 1:
            return 'You can see no further.'
        our_result = self.describe(lifeform, depth)
        return our_result + ' ' + connection_result

    def aura_descriptions(self, lifeform, acuity, sense):
        '''Used for all aura descriptions'''
        for x in self.dungeon.get_applicable_auras(self):
            yield x.brief_inspect(lifeform, acuity, sense)

    def decoration_descriptions(self, lifeform, acuity, sense):
        '''used to describe non-decoration contents'''
        for x in self.contents:
            if isinstance(x, Decoration):
                yield x.brief_inspect(lifeform, acuity, sense)

    def container_descriptions(self, lifeform, acuity, sense):
        '''used to describe non-decoration contents'''
        for x in self.contents:
            if not isinstance(x, Decoration) and not isinstance(x, erukar.engine.lifeforms.Lifeform):
                yield x.brief_inspect(lifeform, acuity, sense)

    def directional_descriptions(self, lifeform, acuity, sense):
        for d in self.connections:
            if self.connections[d].is_door() and self.connections[d].can_see_or_sense(lifeform):
                yield '{:8s} {}'.format(d.name, self.connections[d].peek(d, lifeform))

    def threat_descriptions(self, lifeform, acuity, sense):
        for content in self.contents:
            if isinstance(content, erukar.engine.lifeforms.Lifeform) and content is not lifeform:
                yield content.describe_as_threat(lifeform, acuity, sense)

    def on_start(self, *_):
        '''Called when the Instance has decorated and is actually starting'''
        for content in self.contents:
            content.on_start(self)

    def peek(self, lifeform, acuity, sense):
        '''Used for peeking NESW during on_inspect'''
        light_mod = self.calculate_luminosity()
        if light_mod <= 0.01: return 'The chamber in this direction is completely dark.'
        desc = list(self.threat_descriptions(lifeform, acu, sen))
        desc.insert(self.describe(lifeform),0)
        return ' '.join(desc)

    def on_inspect(self, lifeform, acuity, sense):
        '''Used exclusively for inspecting the current room'''
        light_mod = self.calculate_luminosity()
        acu, sen = acuity * light_mod, sense
        if light_mod <= 0.01:
            return 'This room is completely dark.'
        threats = ' '.join(list(self.threat_descriptions(lifeform, acu, sen)))
        auras = ' '.join(list(self.aura_descriptions(lifeform, acu, sen)))
        self_desc = self.describe(lifeform)
        container = ' '.join(list(self.container_descriptions(lifeform, acu, sen)))
        peeks = '\n'.join(list(self.directional_descriptions(lifeform, acu, sen)))
        return '\n\n'.join(x for x in [threats,auras,self_desc,container,peeks] if x is not '')

    def describe(self, lifeform, depth=0):
        '''Room Descriptions'''
        acu, sen = (lifeform.calculate_effective_stat(x, depth) for x in ['acuity', 'sense'])
        describable_contents = list(self.decoration_descriptions(lifeform, acu, sen))
        if self.floor is not None:
            describable_contents.insert(0, self.floor.brief_inspect(lifeform, acu, sen))
        return ' '.join(describable_contents)

    def connect_room(self, direction, other_room, door=None):
        if other_room is not self:
            self.connections[direction] = Passage(wall=Surface(), room=other_room, door=door)

    def invert_direction(self, direction):
        return Direction( (direction.value + 2) % 4 )

    def get_in_direction(self, direction):
        return self.connections[direction]

    def coestablish_connection(self, direction, other_room, door=None):
        '''Establishes a connection to both rooms'''
        self.connect_room(direction, other_room, door)
        other_room.connect_room(self.invert_direction(direction), self, door)

    def add_door(self, direction, door):
        '''Adds a door and sets it up with the next room appropriately'''
        self.connections[direction].door = door
        other_dir = self.invert_direction(direction)
        self.connections[direction].room.connections[other_dir].door = door

    def content_alias_or_description(self, item, give_alias):
        return item.describe() if not give_alias else item.alias()

    def generate_direction_descriptions(self, lifeform):
        '''Generator for creating a list of directional descriptions'''
        for direction in self.connections:
            res = self.inspect_peek(direction, lifeform)
            if res is not None:
                yield '\n{0}:\t{1}'.format(direction.name, res)

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
            yield self.connections[direction].wall

    def wall_directions(self):
        '''Generator for getting the directions which contain only walls'''
        for direction in self.connections:
            passage = self.connections[direction]
            if passage.room is None and passage.door is None:
                yield direction


    def get_visible_contents(self, acuity, lifeform=None):
        '''
        The actual acuity score is the flat Acuity score multiplied by the room's
        luminosity coefficient, which ranges from 0.0 (pitch black, very rare) to 1.0
        (absolute brightness.) The scalar value is a value which is used to reduce
        the acu_score further and diminishes at a rate of 0.5 per room.
        '''
        return [x for x in self.contents if x.necessary_acuity() <= acuity and x is not lifeform]

    def get_sensed_contents(self, sense, lifeform=None):
        return [x for x in self.contents if x.necessary_sense() <= sense and x is not lifeform]
