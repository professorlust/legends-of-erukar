from ..base.Mineral import Mineral
from erukar.system.engine import Observation
import erukar


class Ceramic(Mineral):
    Probability = 200
    Desirability = 0.25

    InventoryName = 'Ceramic'
    InventoryDescription = 'Reduces durability to 10%; Lowers weight by 60%'

    DurabilityMultiplier = 0.1
    WeightMultiplier = 0.1
    PriceMultiplier = 0.1

    MitigationMultipliers = {
        'bludgeoning': (1, 2),
        'slashing': (0.2, 4),
        'piercing': (1, 0)
    }

    PermittedEntities = [
        erukar.system.inventory.SwordWeapon,
        erukar.system.inventory.PolearmWeapon,
        erukar.system.inventory.SimpleWeapon,
        erukar.system.Armor,
    ]
