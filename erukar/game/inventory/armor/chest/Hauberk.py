from erukar.engine.inventory.Armor import Armor

class Hauberk(Armor):
    EquipmentLocations = ['chest']
    BaseName="Hauberk"
    Probability = 1

    BaseWeight = 7.5
    BasePrice = 65
    InventoryDescription = "Hauberks are large shirts typically made of chainmail or interlocking metal plates. Due to the time they take to produce, they are often fairly expensive."

    DamageMitigations = {
        # type, mitigation percent, glancing range
        'slashing': (0.12, 6),
        'piercing': (0.075, 3)
    }

    def __init__(self):
        super().__init__("Hauberk")
