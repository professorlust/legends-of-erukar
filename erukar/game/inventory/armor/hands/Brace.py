from erukar.engine.inventory.Armor import Armor

class Brace(Armor):
    EquipmentLocations = ['arms']
    BaseName="Brace"
    Probability = 1
    BaseWeight = 1.0

    def __init__(self):
        super().__init__("Brace")
