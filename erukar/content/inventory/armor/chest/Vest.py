from erukar.system.engine import Armor

class Vest(Armor):
    EquipmentLocations = ['chest']
    BaseName="Vest"
    Probability = 1

    InventoryDescription = "Vest todo"
    BasePrice = 30
    BaseWeight = 1.5

    ArmorClass = Armor.Light
    EvasionPenalty = 0.00
    AttackPenalty = 0.00
    DamageMitigations = {
        'piercing': (0.00, 0),
        'slashing': (0.10, 4),
        'bludgeoning': (0.00, 0)
    }
