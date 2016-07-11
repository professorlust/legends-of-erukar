from erukar.game.modifiers.RoomModifier import RoomModifier
from erukar.engine.environment import *
from erukar.engine.factories.ModuleDecorator import ModuleDecorator
import random

class Table(RoomModifier):
    Probability = 1
    materials = [
        'birch',
        'poplar',
        'maple',
        'ash',
        'mahogany',
        'walnut',
        'metallic']
    conditions = [
        "The table seems to have been made recently.",
        "The legs of the table are uneven lengths, leading it to wobble.",
        "It appears to have been used quite recently.",
        "It is falling into a state of disrepair.",
        "It is barely structurally viable."]
    table_top_conditions = [
        "The table has little to nothing on top of it.",
        "The top of the table is organized neatly.",
        "The top of table is cluttered with scraps of papers and notes."]
    alias_base='{0} {1} table'
    broad_result_base='There is a {0} table to the {1} of the room.'
    inspect_result_base='This table is made of {0}. {1}'
    top_alias_base='{0} table top'

    def __init__(self, material=None):
        if material is None:
            material = random.choice(Table.materials)
        self.material = material
        self.condition = random.choice(Table.conditions)

    def apply_to(self, room):
        self.create_table_decoration(room)
        self.create_table_top(room)

    def create_table_decoration(self, room):
        try:
            location = random.choice(list(room.wall_directions())).name
        except:
            location = 'center'
        deco = Container(aliases=[Table.alias_base.format(location, self.material)], \
            broad_results = Table.broad_result_base.format(self.material, location),
            inspect_results=Table.inspect_result_base.format(self.material, self.condition))
        room.add(deco)

    def create_table_top(self, room):
        table_top_condition = random.choice(Table.table_top_conditions)
        top = Container(aliases=[Table.top_alias_base.format(self.material)],\
            broad_results='',\
            inspect_results=table_top_condition)
        r = ModuleDecorator('erukar.game.inventory', None)
        addition = r.create_one()
        top.add(addition)
        room.add(top)
