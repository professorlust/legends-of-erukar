from erukar.system.engine import Armor

class Cuirass(Armor):
    EquipmentLocations = ['chest']
    BaseName="Cuirass"
    Probability = 1

    BaseWeight = 25.0
    BasePrice = 450
    InventoryDescription = "Cuirass description todo"

    ArmorClass = Armor.Medium
    EvasionPenalty = 0.05
    AttackPenalty = 0.05
    DamageMitigations = {
        'piercing': (0.25, 10),
        'slashing': (0.25, 10),
        'bludgeoning': (0.10, 5)
    }
