from erukar.game.modifiers.material.base.Mineral import Mineral

class Glass(Mineral):
    Probability = 0.05
    Desirability = 0.5

    PriceMultiplier = 2.3
    WeightMultiplier = 0.8
    DurabilityMultiplier = 0.3

    InventoryName = "Glass"
    InventoryDescription = 'Reinforced glass, though exceedingly brittle, is light and often modified with various colors as a status symbol'
