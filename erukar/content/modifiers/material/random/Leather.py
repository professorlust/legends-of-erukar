from ..base.Cloth import Cloth
from erukar.system.engine import Observation, Weapon, Armor
import erukar


class Leather(Cloth):
    ProhibitedEntities = [Weapon]
    PermittedEntities = [Armor]
    Probability = 0.05
    Desirability = 2.0

    WeightMultiplier = 0.5
    DurabilityMultiplier = 1.5
    FlexibilityMultiplier = 0.25

    MitigationMultipliers = {
        'bludgeoning': (0.3,0.7),
        'slashing': (1.1, 1.2),
        'piercing': (1.1, 1.2),
    }

    InventoryDescription = "Provides high mobility and durability at the cost of lowered protection"
    InventoryName = "Leather"

    Glances = [
        Observation(acuity=5, sense=0, result="that has been crafted with tanned leather")
    ]

    Inspects = [
        Observation(acuity=0, sense=0, result="The {BaseType} has been created with a tanned leather.")
    ]

    PermittedEntities = [
        erukar.system.Armor
    ]
