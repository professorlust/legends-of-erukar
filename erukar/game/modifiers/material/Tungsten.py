from erukar.game.modifiers.MaterialModifier import MaterialModifier

class Tungsten(MaterialModifier):
    Probability = 0.05
    Desirability = 2.0

    WeightMultiplier = 4.5
    DurabilityMultiplier = 5.2
    PriceMultiplier = 3.5

    MitigationMultipliers = {
        'fire': (3, 5.0)
    }

    InventoryDescription = "Heavy metal which is capable of dissipating high temperatures better than most other metals"
    InventoryName = "Tungeten"
