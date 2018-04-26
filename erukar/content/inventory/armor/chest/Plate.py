from erukar.system.engine import Armor

class Plate(Armor):
    EquipmentLocations = ['chest']
    BaseName="Plate"
    Probability = 1

    InventoryDescription = "A full chest plate is capable of mitigating or glancing most blows, but is cumbersome to wear"
    BasePrice = 1600
    BaseWeight = 55

    ArmorClass = Armor.Heavy
    EvasionPenalty = 0.15
    AttackPenalty = 0.10
    DamageMitigations = {
        'piercing': (0.40, 16),
        'slashing': (0.40, 16),
        'bludgeoning': (0.20, 8)
    }
