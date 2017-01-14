from erukar.engine.inventory.Armor import Armor

class Sprinters(Armor):
    EquipmentLocations = ['feet']
    BaseName="Sprinters"
    Probability = 1
    BaseWeight = 1.2

    def __init__(self):
        super().__init__("Sprinters")
