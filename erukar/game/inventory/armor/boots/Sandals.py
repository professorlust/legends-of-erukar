from erukar.engine.inventory.Armor import Armor

class Sandals(Armor):
    EquipmentLocations = ['feet']
    BaseName="Sandals"
    Probability = 1

    BaseWeight = 0.5

    def __init__(self):
        super().__init__("Sandals")
