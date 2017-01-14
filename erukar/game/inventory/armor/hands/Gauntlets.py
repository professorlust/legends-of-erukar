from erukar.engine.inventory.Armor import Armor

class Gauntlets(Armor):
    EquipmentLocations = ['arms']
    BaseName="Gauntlets"
    Probability = 1
    BaseWeight = 4.3

    def __init__(self):
        super().__init__("Gauntlets")
