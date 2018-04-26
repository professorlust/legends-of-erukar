from erukar.system.engine import Armor

class Mask(Armor):
    EquipmentLocations = ['head']
    BaseName="Mask"
    Probability = 1

    ArmorClass = Armor.Light
    BasePrice = 10
    BaseWeight = 0.2
    DamageMitigations = {
    }
