from erukar.engine.inventory.Armor import Armor

class Plate(Armor):
    EquipmentLocations = ['chest']
    BaseName="Plate"
    Probability = 1
    BaseWeight = 9.7

    def __init__(self):
        super().__init__("Plate")
