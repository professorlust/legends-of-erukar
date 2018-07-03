from ..base.Cloth import Cloth
from erukar.system.engine import Observation, Weapon
import erukar


class StuddedLeather(Cloth):
    ProhibitedEntities = [Weapon]
    Probability = 0.05
    Desirability = 2.0

    WeightMultiplier = 0.7
    DurabilityMultiplier = 1.7
    FlexibilityMultiplier = 0.35

    MitigationMultipliers = {
        'bludgeoning': (0.3,0.7),
        'slashing': (1.3, 1.5),
        'piercing': (1.2, 1.3),
    }

    InventoryDescription = "Provides better slashing and piercing protection other standard leather"
    InventoryName = "Studded Leather"

    PermittedEntities = [
        erukar.system.Armor
    ]
