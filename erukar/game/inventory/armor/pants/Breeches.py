from erukar.engine.inventory.Armor import Armor

class Breeches(Armor):
    EquipmentLocations = ['legs']
    BaseName="Breeches"
    Probability = 1
    BaseWeight = 1.2

    def __init__(self):
        super().__init__("Breeches")
