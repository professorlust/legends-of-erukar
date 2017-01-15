from erukar.game.modifiers.MaterialModifier import MaterialModifier
from erukar import Weapon

class StuddedLeather(MaterialModifier):
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
