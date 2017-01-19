from erukar.game.modifiers.material.base.Metal import Metal
from erukar.engine.model.Observation import Observation

class Steel(Metal):
    Probability = 100
    Desirability = 2.0

    InventoryDescription = "Strong, sturdy alloy; +10% durability"
    InventoryName = "Steel"

    PriceMultiplier = 6.7
    WeightMultiplier = 2.1
    DurabilityMultiplier = 9.5

    Glances = [
        Observation(acuity=5, sense=0, result="with a metallic {EssentialPart}"),
        Observation(acuity=20, sense=0, result="with a steel {EssentialPart}")
    ]

    Inspects = [
        Observation(acuity=5, sense=0, result="The {EssentialPart} appears to be forged with some sort of metal."),
        Observation(acuity=20, sense=0, result="The {EssentialPart} has been forged from a steel alloy.")
    ]
