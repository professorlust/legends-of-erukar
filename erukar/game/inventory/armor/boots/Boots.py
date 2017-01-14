from erukar.engine.inventory.Armor import Armor

class Boots(Armor):
    EquipmentLocations = ['feet']
    Probability = 1
    BaseName = "Boots"

    BaseWeight = 1.4

    def __init__(self):
        super().__init__("Boots")
