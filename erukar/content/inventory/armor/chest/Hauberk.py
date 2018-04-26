from erukar.system.engine import Armor

class Hauberk(Armor):
    EquipmentLocations = ['chest']
    BaseName="Hauberk"
    Probability = 1

    BaseWeight = 14
    BasePrice = 380
    InventoryDescription = "Hauberks are large shirts typically made of chainmail or interlocking metal plates. Due to the time they take to produce, they are often fairly expensive."

    ArmorClass = Armor.Medium
    EvasionPenalty = 0.05
    DamageMitigations = {
        'piercing': (0.25, 10),
        'slashing': (0.25, 10)
    }
