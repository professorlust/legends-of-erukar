from erukar.game.modifiers.MaterialModifier import MaterialModifier
from erukar.engine.model.Observation import Observation

class Salericite(MaterialModifier):
    Probability = 0.05
    Desirability = 8.0

    InventoryDescription = "A black and orange alloy radiating positive energies; enhances outward effects by 25%"
    InventoryName = "Salericite"

    PriceMultiplier = 33
    WeightMultiplier = 1.8
    DurabilityMultiplier = 1.0

    Glances = [
        Observation(acuity=5, sense=0, result="with a black {EssentialPart}"),
        Observation(acuity=10, sense=0, result="with a black {EssentialPart} which shimmers an orangish glare"),
        Observation(acuity=0, sense=7, result="with a slightly magical {EssentialPart}"),
        Observation(acuity=35, sense=7, result="with a black Salericite {EssentialPart} which reflects an orangish glare")
    ]

    Inspects = [
        Observation(acuity=5, sense=0, result="The {EssentialPart} is black."),
        Observation(acuity=10, sense=5, result="The {EssentialPart} is black with an orangish glare; it emanates some sort of magic."),
        Observation(acuity=35, sense=0, result="The {EssentialPart} of the {BaseName} has been forged from a metal known as Salericite."),
        Observation(acuity=35, sense=10, result="The {BaseName}'s {EssentialPart} has been forged from Salericite, a magical ore which is black yet reflects an orangish light at certain angles.")
    ]
