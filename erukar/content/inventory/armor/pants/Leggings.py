from erukar.system.engine import Armor

class Leggings(Armor):
    BaseName="Leggings"
    Probability = 1

    InventoryDescription = "Leggings todo"

    ArmorClass = Armor.Medium
    BasePrice = 120
    BaseWeight = 10
    DamageMitigations = {
        'slashing': (0.20, 12),
        'piercing': (0.10, 6)
    }
