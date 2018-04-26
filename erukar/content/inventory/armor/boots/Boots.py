from erukar.system.engine import Armor

class Boots(Armor):
    EquipmentLocations = ['feet']
    Probability = 1
    BaseName = "Boots"

    BaseWeight = 1.8
    BasePrice = 50

    ArmorClass = Armor.Medium
    EvasionPenalty = 0.05
    DamageMitigations = {
        'bludgeoning': (0.10, 4),
        'piercing': (0.10, 4),
        'slashing': (0.07, 4)
    }
