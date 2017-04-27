from erukar.engine.model.Containable import Containable
from erukar.engine.model.Direction import Direction
from erukar.engine.environment.Passage import Passage
from erukar.engine.environment.Surface import Surface
from erukar.engine.environment.Container import Container
from erukar.engine.environment.Door import Door
from erukar.engine.environment.Decoration import Decoration
from erukar.engine.model.Describable import Describable
from erukar.engine.model.Observation import Observation
import erukar, random
from enum import Enum

class Room(Containable):
    SelfDescription = "This room is fairly large."
    DecoDescription = "You see {}."
    ContainerDescription = "In the room you see {}."
    Glances = [
        Observation(acuity=0, sense=0, result="This is a room.")
    ]

    def __init__(self, dungeon, coordinates=(0,0), shape=None, dimensions=(1, 1)):
        super().__init__([])
        self.linearity = 0
        self.dungeon = dungeon
        self.shape = shape if shape is not None else erukar.engine.environment.roomshapes.Rectangle
        self.width, self.height = dimensions
        self.is_valid = self.dungeon.add_room(self, coordinates)
        self.floor = None
        self.ceiling = None
        self.coordinates = coordinates
        self.connections = []
        self.visible_in_room_description = False

    def calculate_luminosity(self):
        luminosity = 0
        for aura in self.dungeon.get_applicable_auras(self):
            if hasattr(aura, 'modify_light'):
                decay = aura.get_decay_at(self)
                luminosity += aura.modify_light(decay)
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
        return 'Directional Inspect is under construction'

    def aura_descriptions(self, lifeform, acuity, sense):
        '''Used for all aura descriptions'''
        for x in self.dungeon.get_applicable_auras(self):
            res = x.on_glance(lifeform, acuity, sense)
            if res is not '':
                yield res

    def decoration_descriptions(self, lifeform, acuity, sense):
        '''used to describe non-decoration contents'''
        for x in self.contents:
            if not x.is_detected(acuity, sense):
                continue

            if isinstance(x, Decoration) or isinstance(x, Container):
                res = self.mutate(x.on_glance(lifeform, acuity, sense))
                if res is not '':
                    yield res

    def container_descriptions(self, lifeform, acuity, sense):
        '''used to describe non-decoration contents'''
        for x in self.contents:
            if not x.is_detected(acuity, sense):
                continue

            if not isinstance(x, Decoration) and not isinstance(x, erukar.engine.lifeforms.Lifeform) and not isinstance(x, Container):
                res = x.on_glance(lifeform, acuity, sense)
                if res is not '':
                    yield res

    def directional_descriptions(self, lifeform, acuity, sense):
        for connection in self.connections:
            if connection.is_valid() and connection.can_detect(lifeform):
                yield '{:8s} {}'.format(connection.describe(self), connection.peek(lifeform, acuity, sense))

    def threat_descriptions(self, lifeform, acuity, sense):
        for content in self.detected_lifeforms(lifeform, acuity, sense):
            yield content.describe_as_threat(lifeform, acuity, sense)

    def detected_contents(self, lifeform, acuity, sense):
        for content in self.contents:
            if content.is_detected(acuity, sense):
                yield content

    def detected_lifeforms(self, lifeform, acuity, sense):
        for content in self.detected_contents(lifeform, acuity, sense):
            if isinstance(content, erukar.engine.lifeforms.Lifeform) and content is not lifeform:
                yield content

    def on_start(self, *_):
        '''Called when the Instance has decorated and is actually starting'''
        for content in self.contents:
            content.on_start(self)

    def peek(self, lifeform, acuity, sense):
        '''Used for peeking NESW during on_inspect'''
        light_mod = self.calculate_luminosity()
        acuity *= self.calculate_luminosity()
        if acuity <= 0 or sense <= 0:
            return 'The chamber in this direction is completely dark.'
        desc = [x for x in self.threat_descriptions(lifeform, acuity, sense) if x is not '']
        return Describable.on_glance(self, lifeform, acuity, sense) + ' ' + Describable.erjoin(desc)

    def on_inspect(self, lifeform, acuity, sense):
        '''Used exclusively for inspecting the current room'''
        light_mod = self.calculate_luminosity()
        acu, sen = acuity * light_mod, sense
        if light_mod <= 0.01:
            return 'This room is completely dark.'
        threats = ' '.join(list(self.threat_descriptions(lifeform, acu, sen)))
        auras = ' '.join(list(self.aura_descriptions(lifeform, acu, sen))[:3])
        self_desc = self.describe(lifeform, acu, sen)
        container_desc = Describable.erjoin(list(self.container_descriptions(lifeform, acu, sen)))
        container = self.ContainerDescription.format(container_desc) if len(container_desc) > 0 else ''
        peeks = '\n'.join(list(self.directional_descriptions(lifeform, acu, sen)))
        return '\n\n'.join(x for x in [threats,auras,self_desc,container,peeks] if x is not '')

    def append_if_nonempty(self, collection, string, with_format):
        if string is not '':
            collection.append(with_format.format(string))

    def surfaces_at_a_glance(self, lifeform, acu, sen):
        nonempty_surfaces  = []
        floor = '' if not self.floor else self.floor.on_glance(lifeform, acu, sen)
        self.append_if_nonempty(nonempty_surfaces, floor, 'the floor is {}')
        ceiling = '' if not self.ceiling else self.ceiling.on_glance(lifeform, acu, sen)
        self.append_if_nonempty(nonempty_surfaces, ceiling, 'the ceiling is {}')
        walls = list(set(self.connections[x].wall.on_glance(lifeform, acu, sen) for x in self.connections if self.connections[x].wall))
        self.append_if_nonempty(nonempty_surfaces, Describable.erjoin(walls), 'the walls are {}')

        result = Describable.erjoin(nonempty_surfaces)
        return result.capitalize() + '.' if result is not '' else ''

    def describe(self, lifeform, acu, sen, depth=0):
        '''Room Descriptions'''
        describable_contents = [x for x in self.decoration_descriptions(lifeform, acu, sen) if x is not '']

        self_describe = self.SelfDescription
        if depth == 0:
            self_describe = ' '.join([self_describe, self.surfaces_at_a_glance(lifeform, acu, sen)])
        if len(describable_contents) > 0:
            return self_describe + ' ' + self.DecoDescription.format(Describable.erjoin(describable_contents[:3]))
        return self_describe

    def connect(self, other_room, door=None):
        '''Establishes a connection to both rooms'''
        new_passage = Passage(rooms=[self, other_room], door=door)
        self.add_passage(new_passage)
        other_room.add_passage(new_passage)

    def add_passage(self, passage):
        if passage.has_door(): self.add(passage.door)
        self.connections.append(passage)

    def adjacent_rooms(self):
        '''Generator which yields rooms we can see into from this one'''
        for c in self.connections:
            if c.is_valid():
                yield c

    def center(self):
        return self.shape.center(self)

    def get_object_by_uuid(self, uuid):
        for connection in self.connections:
            if connection.uuid is uuid:
                yield connection
                raise StopIteration

        for found in super().get_object_by_uuid(uuid):
            yield found
