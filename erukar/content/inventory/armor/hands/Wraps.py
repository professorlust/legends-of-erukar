from erukar.system.engine import Armor

class Wraps(Armor):
    EquipmentLocations = ['arms']
    BaseName="Wraps"
    Probability = 1

    InventoryDescription = "Wraps todo"
    BasePrice = 10
    BaseWeight = 0.2

    ArmorClass = Armor.Light
    EvasionPenalty = -0.05
    DamageMitigations = {
    }
