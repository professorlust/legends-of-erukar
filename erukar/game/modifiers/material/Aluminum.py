from erukar.game.modifiers.MaterialModifier import MaterialModifier
from erukar.engine.model.Observation import Observation

class Aluminum(MaterialModifier):
    Probability = 200
    ProbabilityFromFabrication = 0.1
    Desirability = 1.0

    PriceMultiplier = 1.5
    WeightMultiplier = 0.7
    DurabilityMultiplier = 0.8

    InventoryName = 'Aluminum'
    InventoryDescription = 'Lightweight metal lowers weight by 30% but is highly pliable, reducing durability by 20%'

    Glances = [
        Observation(acuity=5, sense=0, result="with a metallic gray {EssentialPart}"),
        Observation(acuity=10, sense=0, result="with an unpolished metallic gray {EssentialPart}"),
        Observation(acuity=10, sense=10, result="with a lightweight, unpolished metallic gray {EssentialPart}"),
        Observation(acuity=35, sense=0, result="with an aluminum {EssentialPart}")
    ]

    Inspects = [
        Observation(acuity=5, sense=0, result="The {EssentialPart} has been forged with some sort of worked, gray metal."),
        Observation(acuity=10, sense=5, result="The {BaseName} is lighter than you anticipate."),
        Observation(acuity=35, sense=0, result="The {EssentialPart} of the {BaseName} has been forged from an unpolished aluminum."),
        Observation(acuity=35, sense=5, result="The {EssentialPart} of the {BaseName} is very light, as it has been forged from some sort of unpolished aluminum."),
        Observation(acuity=35, sense=10, result="The {BaseName}'s {EssentialPart} has been forged from a sturdy and lightweight, yet unpolished, aluminum.")
    ]
