from .Inspect import Inspect

class Glance(Inspect):
    NeedsArgs = False
    ActionPointCost = 1

    RadiusAroundInspection = 3
    FogOfWarScalar = 1.0
    ObservationPenalty = 0.30
