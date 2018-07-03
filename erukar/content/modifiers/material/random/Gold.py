from ..base.Metal import Metal
from erukar.system.engine import Observation
import erukar


class Gold(Metal):
    Probability = 0.05
    Desirability = 8.0

    PriceMultiplier = 35
    WeightMultiplier = 3.0
    DurabilityMultiplier = 0.9

    InventoryName = "Gold"
    InventoryDescription = 'Gold\'s status as a precious commodity stems from its rarity, not its durability.'

    PermittedEntities = [
        erukar.system.Weapon,
        erukar.system.Ammunition,
        erukar.system.Armor
    ]
