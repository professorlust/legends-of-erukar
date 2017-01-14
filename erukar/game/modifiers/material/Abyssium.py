from erukar.game.modifiers.MaterialModifier import MaterialModifier
from erukar.engine.model.Observation import Observation

class Abyssium(MaterialModifier):
    Probability = 200
    ProbabilityFromSanctity = -1.0
    Desirability = 2.0

    PriceMultiplier = 20
    WeightMultiplier = 1.2
    DurabilityMultiplier = 2.5

    InventoryDescription = "Rare ore mined from Demonic Ruins; predilection towards Unholiness and Curses"
    InventoryName = "Abyssium"

    Glances = [
        Observation(acuity=5, sense=0, result="with a dark red {EssentialPart}"),
        Observation(acuity=10, sense=10, result="with an unholy, dark red {EssentialPart}"),
        Observation(acuity=35, sense=0, result="with an Abyssium {EssentialPart}")
    ]

    Inspects = [
        Observation(acuity=5, sense=0, result="The {EssentialPart} appears to be carved out of a dark, reddish black stone."),
        Observation(acuity=10, sense=0, result="The {EssentialPart} appears to be carved out of a dark, reddish black stone that seems to lightly glow a faint red light."),
        Observation(acuity=10, sense=10, result="The {EssentialPart} appears to be carved out of some sort of unholy, reddish black stone that glows a faint red light."),
        Observation(acuity=35, sense=0, result="The {EssentialPart} is made of a blood red stone known as \"Abyssium\".")
    ]
