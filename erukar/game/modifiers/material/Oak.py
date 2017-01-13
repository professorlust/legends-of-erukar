from erukar.game.modifiers.MaterialModifier import MaterialModifier
from erukar.engine.model.Observation import Observation

class Oak(MaterialModifier):
    Probability = 0.05
    Desirability = 1.0
    InventoryName = "Oak"

    DurabilityMultiplier = 0.7
    WeightMultiplier = 0.6

    InventoryDescription = "A light tan, soft wood; preferred by mages for use in wands."

    Glances = [
        Observation(acuity=5, sense=0, result="with a wooden {EssentialPart}"),
        Observation(acuity=20, sense=0, result="with a oaken {EssentialPart}")
    ]

    Inspects = [
        Observation(acuity=5, sense=0, result="The {EssentialPart} has been carved from wood."),
        Observation(acuity=20, sense=0, result="The {EssentialPart} has been carved from white oak.")
    ]
