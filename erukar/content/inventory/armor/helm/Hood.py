from erukar.system.engine import Armor

class Hood(Armor):
    EquipmentLocations = ['head']
    BaseName="Hood"
    Probability = 1

    ArmorClass = Armor.Light
    BasePrice = 10
    BaseWeight = 0.2
    DamageMitigations = {
    }
