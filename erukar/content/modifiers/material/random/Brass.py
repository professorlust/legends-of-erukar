from ..base.Metal import Metal
from erukar.system.engine import Observation
import erukar


class Brass(Metal):
    Probability = 200
    Desirability = 1.0

    InventoryName = 'Brass'
    InventoryDescription = 'Decreases weight by 40%; Decreases Durability by 35%'

    PriceMultiplier = 1.2
    WeightMultiplier = 0.6
    DurabilityMultiplier = 0.65

    Glances = [
        Observation(acuity=5, sense=0, result="with a metallic yellow {BaseName}"),
        Observation(acuity=10, sense=0, result="with an polished yellow metal {EssentialPart}"),
        Observation(acuity=10, sense=10, result="with a light, polished metallic yellow {EssentialPart}"),
        Observation(acuity=35, sense=0, result="with an brass {EssentialPart}")
    ]

    Inspects = [
        Observation(acuity=5, sense=0, result="The {EssentialPart} has been made of a yellow metal."),
        Observation(acuity=5, sense=5, result="The {EssentialPart} is made of an expensive metal."),
        Observation(acuity=10, sense=0, result="The {EssentialPart} is made with a light, polished yellow metal"),
        Observation(acuity=35, sense=0, result="The {EssentialPart} of the {BaseName} has been forged from Brass."),
        Observation(acuity=35, sense=5, result="The {EssentialPart} of the {BaseName} is light, as it has been forged polished brass."),
        Observation(acuity=35, sense=10, result="The {BaseName}'s {EssentialPart} has been forged from a resilient and lightweight brass.")
    ]

    PermittedEntities = [
        erukar.system.Weapon,
        erukar.system.Ammunition,
        erukar.system.Armor
    ]
