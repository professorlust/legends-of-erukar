from erukar.game.modifiers.RoomModifier import RoomModifier
from erukar.engine.environment.Surface import Surface
from erukar.engine.model.Observation import Observation


class ClayCeiling(RoomModifier):
    ProbabilityFromFabrication = 0.4

    Glances = [
        Observation(acuity=0, sense=0, result="made of clay"),
    ]

    Inspects = [
        Observation(acuity=0, sense=0, result="The ceiling is made of clay.")
    ]

    def apply_to(self, room):
        room.ceiling = Surface()
        ceiling.Glances = ceiling.Glances + self.Glances
        ceiling.Inspects = ceiling.Inspects + self.Inspects
