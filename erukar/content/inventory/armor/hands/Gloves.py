from erukar.system.engine import Armor

class Gloves(Armor):
    EquipmentLocations = ['arms']
    BaseName="Gloves"
    Probability = 1

    InventoryDescription = "Gloves todo"
    BasePrice = 25
    BaseWeight = 0.5

    ArmorClass = Armor.Medium
    DamageMitigations = {
        'piercing': (0.07, 3),
        'slashing': (0.07, 3),
    }
