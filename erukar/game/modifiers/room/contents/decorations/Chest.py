from erukar.engine.environment import *
from erukar.game.modifiers.RoomModifier import RoomModifier
from erukar.engine.factories.ModuleDecorator import ModuleDecorator
from erukar.engine.model.Observation import Observation
import random

class Chest(RoomModifier):
    MultipleItemProbability = 0.4
    SingleItemProbabilityWeight = 0.2
    ProbabilityFromFabrication = 0.5

    broad_alias_base = 'chest'

    BaseGlances = [
        Observation(acuity=3, sense=0, result="a chest")
    ]

    BaseInspects = [
        Observation(acuity=0, sense=0, result="There is a chest on the {direction} wall of this area{glance_inside_from_inspect}."),
    ]

    def apply_to(self, room):
        # Create the Chest
        chest = Container(aliases=[self.broad_alias_base])
        chest.direction = self.random_wall(room)
        chest.on_inspect_preface = '. Inside of the chest you see {}'
        chest.on_glance_preference = ' with {} inside'
        chest.Glances = Chest.BaseGlances
        chest.Inspects = Chest.BaseInspects
        chest.contents_visible = False
        r = ModuleDecorator('erukar.game.inventory', self.generation_parameters)
        for i in range(random.randint(3,8)):
            chest.contents.append(r.create_one())
        room.add(chest)
