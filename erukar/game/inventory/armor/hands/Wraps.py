from erukar.engine.inventory.Armor import Armor

class Wraps(Armor):
    EquipmentLocations = ['arms']
    BaseName="Wraps"
    Probability = 1
    BaseWeight = 0.2

    def __init__(self):
        super().__init__("Wraps")
