from erukar.system.engine import Armor

class Robes(Armor):
    EquipmentLocations = ['chest']
    BaseName="Robes"
    Probability = 1

    InventoryDescription = "Robes are outerwear which are often used by monks and aracanists."
    BasePrice = 10
    BaseWeight = 0.7

    ArmorClass = Armor.Light
    DamageMitigations = {
        'piercing': (0.00, 0),
        'slashing': (0.01, 2),
        'bludgeoning': (0.00, 0)
    }
