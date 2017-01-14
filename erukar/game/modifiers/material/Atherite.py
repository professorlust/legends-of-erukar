from erukar.game.modifiers.MaterialModifier import MaterialModifier
from erukar.engine.model.Observation import Observation

class Atherite(MaterialModifier):
    Probability = 200
    Desirability = 4.0

    InventoryDescription = "A whitish alloy infused with chaotic energies; enhances random effects by 25%"
    InventoryName = "Atherite"

    PriceMultiplier = 12.5
    WeightMultiplier = 3.1
    DurabilityMultiplier = 1.2

    Glances = [
        Observation(acuity=5, sense=0, result="with a white {EssentialPart}"),
        Observation(acuity=10, sense=0, result="with a whitish {EssentialPart} which shimmers a faint blue light "),
        Observation(acuity=10, sense=10, result="with a slightly magical {EssentialPart}"),
        Observation(acuity=35, sense=0, result="with an white ore called Atherite, the {EssentialPart} shimmers in a faint blue light")
    ]

    Inspects = [
        Observation(acuity=5, sense=0, result="The {EssentialPart} is white with a faint blue sheen."),
        Observation(acuity=10, sense=5, result="The {EssentialPart} is whitish, with a shimmering blue light. A sign of magic."),
        Observation(acuity=35, sense=0, result="The {EssentialPart} of the {BaseName} has been forged from a metal known as Atherite."),
        Observation(acuity=35, sense=10, result="The {BaseName}'s {EssentialPart} has been forged from Atherite, a magical ore which is white and shimmers a blue light; you feel that this weapon possesses some link to magical chaos.")
    ]
