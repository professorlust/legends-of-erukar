from erukar.engine.inventory.Armor import Armor

class Vambrace(Armor):
    EquipmentLocations = ['arms']
    BaseName="Vambrace"
    BaseWeight = 2.0
    Probability = 1

    def __init__(self):
        super().__init__("Vambrace")
