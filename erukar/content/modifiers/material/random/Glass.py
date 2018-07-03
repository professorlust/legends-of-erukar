from ..base.Mineral import Mineral
from erukar.system.engine import Observation
import erukar


class Glass(Mineral):
    Probability = 0.05
    Desirability = 0.5

    PriceMultiplier = 2.3
    WeightMultiplier = 0.8
    DurabilityMultiplier = 0.3

    InventoryName = "Glass"
    InventoryDescription = 'Reinforced glass, though exceedingly brittle, is light and often modified with various colors as a status symbol'

    PermittedEntities = [
        erukar.system.inventory.ArcaneWeapon,
        erukar.system.inventory.SwordWeapon,
        erukar.system.inventory.PolearmWeapon,
        erukar.system.inventory.SimpleWeapon,
        erukar.system.Armor,
    ]
