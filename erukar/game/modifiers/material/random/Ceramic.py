from erukar.game.modifiers.material.base.Mineral import Mineral

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
