from erukar.system.engine import Armor

class Helm(Armor):
    EquipmentLocations = ['head']
    BaseName="Helm"
    Probability = 1

    ArmorClass = Armor.Heavy
    BasePrice = 350
    BaseWeight = 26
    VisionPenalty = 0.25
    DamageMitigations = {
        'piercing': (0.35, 14),
        'slashing': (0.35, 14)
    }
