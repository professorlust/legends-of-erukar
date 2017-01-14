from erukar.engine.inventory.Armor import Armor

class Brigandine(Armor):
    EquipmentLocations = ['chest']
    BaseName="Brigandine"
    Probability = 1
    BaseWeight = 6.6

    def __init__(self):
        super().__init__("Brigandine")
