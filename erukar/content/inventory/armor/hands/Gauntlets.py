from erukar.system.engine import Armor

class Gauntlets(Armor):
    EquipmentLocations = ['arms']
    BaseName="Gauntlets"
    Probability = 1

    InventoryDescription = "Gauntlets todo"
    BasePrice = 180
    BaseWeight = 15

    ArmorClass = Armor.Heavy
    AttackPenalty = 0.10
    DamageMitigations = {
        'piercing': (0.20, 10),
        'slashing': (0.20, 10),
        'bludgeoning': (0.07, 3)
    }
