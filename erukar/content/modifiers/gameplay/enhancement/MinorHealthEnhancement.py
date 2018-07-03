from .HealthEnhancement import HealthEnhancement


class MinorHealthEnhancement(HealthEnhancement):
    Probability = 1
    PriceMod = 1.75

    InventoryName = "Minor Health Enhancement"
    InventoryDescription = 'Increases maximum health by 20'
    InventoryFlavorText = ''
    MaxHealthBonus = 20
