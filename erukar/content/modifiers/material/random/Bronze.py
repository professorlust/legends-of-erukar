from ..base.Metal import Metal
from erukar.system.engine import Observation
import erukar


class Bronze(Metal):
    Probability = 200
    Desirability = 2.0

    PriceMultiplier = 3
    WeightMultiplier = 3.5
    DurabilityMultiplier = 0.9

    InventoryName = 'Bronze'
    InventoryDescription = 'Heavy but cheap metal which is easy to work with'

    Glances = [
        Observation(acuity=5, sense=0, result="with a metallic yellow {BaseName}"),
        Observation(acuity=10, sense=0, result="with a dark, unpolished metal {EssentialPart}"),
        Observation(acuity=10, sense=10, result="with a heavy, unpolished metallic yellow {EssentialPart}"),
        Observation(acuity=35, sense=0, result="with a bronze {EssentialPart}")
    ]

    Inspects = [
        Observation(acuity=5, sense=0, result="The {EssentialPart} has been made of a dark, yellow metal."),
        Observation(acuity=5, sense=5, result="The {EssentialPart} is made with a heavy, yellow metal."),
        Observation(acuity=10, sense=0, result="The {EssentialPart} of this {BaseName} is some sort of dark, unpolished metal which has a hint of yellow tint."),
        Observation(acuity=35, sense=0, result="The dark and dull-yellow {EssentialPart} of the {BaseName} has been forged from Bronze."),
        Observation(acuity=35, sense=10, result="The Bronze {EssentialPart} is unpolished, heavy, and full of imperfections. However, its craftsmanship is top notch.")
    ]

    PermittedEntities = [
        erukar.system.Weapon,
        erukar.system.Ammunition,
        erukar.system.Armor
    ]
