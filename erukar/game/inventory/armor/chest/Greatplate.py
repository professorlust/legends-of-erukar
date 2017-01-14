from erukar.engine.inventory.Armor import Armor

class Greatplate(Armor):
    EquipmentLocations = ['chest']
    BaseName="Greatplate"
    Probability = 1

    BaseWeight = 12.0

    def __init__(self):
        super().__init__("Greatplate")
