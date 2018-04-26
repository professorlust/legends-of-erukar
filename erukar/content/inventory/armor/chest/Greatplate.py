from erukar.system.engine import Armor

class Greatplate(Armor):
    EquipmentLocations = ['chest']
    BaseName="Greatplate"
    Probability = 1

    BaseWeight = 60.0
    BasePrice = 2000
    InventoryDescription = "Greatplates are the heaviest standard platemail available on the market, providing extreme protection despite being heavy and expensive."

    ArmorClass = Armor.Heavy
    EvasionPenalty = 0.20
    AttackPenalty = 0.20
    DamageMitigations = {
        'piercing': (0.50, 20),
        'slashing': (0.50, 20),
        'bludgeoning': (0.25, 10)
    }
