from erukar.game.modifiers.MaterialModifier import MaterialModifier
from erukar.engine.model.Observation import Observation
from erukar import Weapon, Armor

class Chainmail(MaterialModifier):
    ProhibitedEntities = [Weapon]
    PermittedEntities = [Armor]
    Probability = 0.05
    Desirability = 6.0

    PriceMultiplier = 10.0
    WeightMultiplier = 4.0
    DurabilityMultiplier = 4.0
    FlexibilityMultiplier = 1.0 

    MitigationMultipliers = {
        'bludgeoning': (0.1,0.5),
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

