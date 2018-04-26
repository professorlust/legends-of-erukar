from erukar.system.engine import Armor

class Burgonet(Armor):
    EquipmentLocations = ['head']
    BaseName="Burgonet"
    Probability = 1

    ArmorClass = Armor.Heavy
    BasePrice = 320
    BaseWeight = 28
    VisionPenalty = 0.25
    DamageMitigations = {
        'piercing': (0.20, 8),
        'slashing': (0.40, 16),
        'bludgeoning': (0.05, 2)
    }
