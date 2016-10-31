from erukar.game.modifiers.MaterialModifier import MaterialModifier
from erukar.engine.model.Observation import Observation

class Steel(MaterialModifier):
    Probability = 100
    Desirability = 2.0

    InventoryDescription = "Strong, sturdy alloy; +10% durability"
    InventoryName = "Steel"

    Glances = [
        Observation(acuity=5, sense=0, result="with a metallic {EssentialPart}"),
        Observation(acuity=20, sense=0, result="with a steel {EssentialPart}")
    ]

    Inspects = [
        Observation(acuity=5, sense=0, result="The {EssentialPart} appears to be forged with some sort of metal."),
        Observation(acuity=20, sense=0, result="The {EssentialPart} has been forged from a steel alloy.")
    ]
