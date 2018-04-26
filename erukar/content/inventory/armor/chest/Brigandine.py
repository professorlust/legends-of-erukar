from erukar.system.engine import Armor

class Brigandine(Armor):
    EquipmentLocations = ['chest']
    BaseName="Brigandine"
    Probability = 1
    BaseWeight = 12.6
    BasePrice = 400
    InventoryDescription = "Brigandine description todo"

    ArmorClass = Armor.Medium
    EvasionPenalty = 0.05
    DamageMitigations = {
        'piercing': (0.10, 5),
        'slashing': (0.25, 10)
    }
