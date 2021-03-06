from ..base.Metal import Metal
from erukar.system.engine import Observation, Weapon, Armor
import erukar


class Chainmail(Metal):
    ProhibitedEntities = [Weapon]
    PermittedEntities = [Armor]
    Probability = 0.05
    Desirability = 6.0

    PriceMultiplier = 10.0
    WeightMultiplier = 4.0
    DurabilityMultiplier = 4.0
    FlexibilityMultiplier = 1.0

    MitigationMultipliers = {
        'bludgeoning': (0.1, 0.5),
        'slashing': (2, 1.5),
        'piercing': (2, 1.5),
    }

    InventoryDescription = "Provides better mobility, improves piercing/slashing mitigation, reduces bludgeoning mitigation"
    InventoryName = "Chainmail"

    Glances = [
        Observation(acuity=5, sense=0, result="that has been forged with chainmail")
    ]

    Inspects = [
        Observation(acuity=0, sense=0, result="The {BaseType} has been forged with interlocking weaves of chain")
    ]

    PermittedEntities = [
        erukar.system.Armor
    ]
