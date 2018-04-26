from erukar.system.engine import Armor

class Coif(Armor):
    EquipmentLocations = ['head']
    BaseName="Coif"
    Probability = 1

    ArmorClass = Armor.Medium
    BasePrice = 80
    BaseWeight = 3.8
    DamageMitigations = {
        'piercing': (0.30, 12),
        'slashing': (0.10, 4)
    }
