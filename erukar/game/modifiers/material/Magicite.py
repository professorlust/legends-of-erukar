from erukar.game.modifiers.MaterialModifier import MaterialModifier
from erukar.engine.model.Observation import Observation

class Magicite(MaterialModifier):
    Probability = 100
    Desirability = 8.0

    InventoryDescription = "Magically-infused, reddish alloy; enhances magic imbuements by 10%"
    InventoryName = "Magicite"

    Glances = [
        Observation(acuity=5, sense=0, result="with a reddish {EssentialPart}"),
        Observation(acuity=0, sense=10, result="with a magical {EssentialPart}"),
        Observation(acuity=10, sense=10, result="with a reddish, magical {EssentialPart}"),
        Observation(acuity=20, sense=10, result="with ~a_or_an~ {EssentialPart} made of Magicite")
    ]

    Inspects = [
        Observation(acuity=5, sense=0, result="The {EssentialPart} has been crafted with some sort of reddish material."),
        Observation(acuity=0, sense=10, result="The {BaseName} seems to emanate magic."),
        Observation(acuity=10, sense=10, result="The {EssentialPart} has been crafted with some sort of magical, reddish material."),
        Observation(acuity=20, sense=10, result="The {EssentialPart} has been forged and enchanted with Magicite, a magically-infused reddish alloy.")
    ]

