from erukar.system.engine import Armor

class CloseHelm(Armor):
    EquipmentLocations = ['head']
    BaseName="Close Helm"
    Probability = 1

    ArmorClass = Armor.Heavy
    BasePrice = 540
    BaseWeight = 36
    VisionPenalty = 0.50
    DamageMitigations = {
        'piercing': (0.40, 16),
        'slashing': (0.40, 16),
        'bludgeoning': (0.15, 6)
    }
