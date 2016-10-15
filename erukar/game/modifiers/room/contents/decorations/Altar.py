from erukar.engine.model import Modifier
from erukar.engine.environment import *
from erukar.game.modifiers.RoomModifier import RoomModifier
from erukar.engine.factories.ModuleDecorator import ModuleDecorator
from erukar.engine.model.Observation import Observation
import random

class Altar(RoomModifier):
    MultipleItemProbability     = 0.90
    SingleItemProbabilityWeight = 0.2
    ProbabilityFromFabrication  = 0.1
    ProbabilityFromSanctity     = 1.0

    BaseGlances = [
        Observation(acuity=3,  sense=0,  result="an altar"),
        Observation(acuity=0,  sense=5,  result="a smoky smell"),
        Observation(acuity=0,  sense=10, result="the smell of burning incense"),
        Observation(acuity=3,  sense=10, result="an altar and the smell of burning incense"),
        Observation(acuity=20, sense=0,  result="an altar{glance_inside|altar_top}")
    ]

    BaseInspects = [
        Observation(acuity=0,  sense=0,  result="There is an altar on the {direction} wall of this area."),
        Observation(acuity=5,  sense=0,  result="There is an altar to the {direction} in this area. {organizational_state}{glance_inside_from_inspect|altar_top}."),
    ]

    broad_alias_base = 'altar'

    organizational_states = [
        'It is completely cleared off aside from {glance_inside_from_inspect_no_preface|altar_top}',
        'The altar has been cleared off, save for some burning incense',
        'There is an animal carcass on the top of the altar',
        'There are papers with scribbles scattered on top of the altar'
    ]

    def apply_to(self, room):
        direction = self.random_wall(room)

        # Create the Altar proper
        deco = Decoration(aliases=[self.broad_alias_base])
        deco.organizational_state = random.choice(Altar.organizational_states)
        deco.direction = self.random_wall(room)
        deco.Glances = Altar.BaseGlances
        deco.Inspects = Altar.BaseInspects
        deco.altar_top = self.create_altar_top(room)
        room.add(deco)

    def create_altar_top(self, room):
        top = Container(['top of the altar', 'altar top'])
        top.on_inspect_preface = '. On top of the altar you see {}'
        top.on_glance_preface = ' with {} on top'
        top.contents_visible = True
        r = ModuleDecorator('erukar.game.inventory', self.generation_parameters)
        top.contents.append(r.create_one())
        room.add(top)
        return top
