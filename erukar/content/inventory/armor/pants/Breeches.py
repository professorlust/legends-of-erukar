from erukar.system.engine import Armor

class Breeches(Armor):
    EquipmentLocations = ['legs']
    BaseName="Breeches"
    Probability = 1
    InventoryDescription = "Breeches todo"

    ArmorClass = Armor.Light
    BasePrice = 60
    BaseWeight = 1.4
    DamageMitigations = {
        'slashing': (0.10, 6)
    }
