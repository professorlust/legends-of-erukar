from erukar.engine.inventory.Armor import Armor

class Greaves(Armor):
    EquipmentLocations = ['legs']
    BaseName="Greaves"
    Probability = 1
    BaseWeight = 4

    def __init__(self):
        super().__init__("Greaves")
