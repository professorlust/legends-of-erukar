from ..base.Metal import Metal
from erukar.system.engine import Observation
import erukar


class Iron(Metal):
    Probability = 0.05
    Desirability = 1.0
    InventoryName = "Iron"

    PriceMultiplier = 3.1
    WeightMultiplier = 1.5
    DurabilityMultiplier = 2.5

    InventoryName = 'Iron'
    InventoryDescription = 'A strong base metal -- hard to forge and fairly heavy but resilient'

    Glances = [
        Observation(acuity=5, sense=0, result="with a metallic gray {EssentialPart}"),
        Observation(acuity=10, sense=0, result="with an unpolished metallic gray {EssentialPart}"),
        Observation(acuity=10, sense=10, result="with a dull gray, heavy {EssentialPart}"),
        Observation(acuity=35, sense=0, result="with an iron {EssentialPart}")
    ]

    Inspects = [
        Observation(acuity=5, sense=0, result="The {EssentialPart} has been forged with some sort of worked, gray metal."),
        Observation(acuity=10, sense=5, result="The {BaseName} is lighter than you anticipate."),
        Observation(acuity=35, sense=0, result="The {EssentialPart} of the {BaseName} has been forged from an unpolished aluminum."),
        Observation(acuity=35, sense=5, result="The {EssentialPart} of the {BaseName} is very light, as it has been forged from some sort of unpolished aluminum."),
        Observation(acuity=35, sense=10, result="The {BaseName}'s {EssentialPart} has been forged from a sturdy and lightweight, yet unpolished, aluminum.")
    ]

    PermittedEntities = [
        erukar.system.Weapon,
        erukar.system.Ammunition,
        erukar.system.Armor
    ]
