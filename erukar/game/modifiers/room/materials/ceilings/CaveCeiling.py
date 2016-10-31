from erukar.game.modifiers.RoomModifier import RoomModifier
from erukar.engine.environment.Surface import Surface
from erukar.engine.model.Observation import Observation


class CaveCeiling(RoomModifier):
    ProbabilityFromFabrication = -0.5
    ProbabilityFromAltitude = -0.5

    Glances = [
        Observation(acuity=0, sense=0, result="cavernlike"),
    ]

    Inspects = [
        Observation(acuity=0, sense=0, result="The ceiling is cavernlike.")
    ]

    def apply_to(self, room):
        room.ceiling = Surface()
        room.ceiling.Glances = self.Glances
        room.ceiling.Inspects = self.Inspects
