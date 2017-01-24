from erukar.game.modifiers.RoomModifier import RoomModifier
from erukar.engine.environment import *
from erukar.engine.factories.ModuleDecorator import ModuleDecorator
import erukar, random

class Table(RoomModifier):
    Probability = 0.2
    ProbabilityFromFabrication = 0.8

    materials = [
        'birch',
        'poplar',
        'maple',
        'ash',
        'mahogany',
        'walnut',
        'metallic']

    def __init__(self):
        self.material = random.choice(Table.materials)

    def apply_to(self, room):
        self.create_table_decoration(room)
        self.create_table_top(room)

    def create_table_decoration(self, room):
        deco = Decoration(aliases=['{} table proper'.format(self.material)])
        deco.material = self.material
        deco.BriefDescription = "a table to the {location}"
        deco.location = self.random_wall(room)
        room.add(deco)

    def create_table_top(self, room):
        top = Container(aliases=['{} table top'.format(self.material), 'top of {} table'.format(self.material)])
        top.visible_in_room_description = False
        c = erukar.game.inventory.consumables.Candle()
        top.BriefDescription = "The table top is completely bare."
        top.ContentDescription = "On top of the table, you find {}."
        top.add(c)
        room.add(top)
