from erukar.engine.inventory.Armor import Armor

class Footguards(Armor):
    EquipmentLocations = ['feet']
    BaseName="Footguards"
    BaseWeight = 1.5
    Probability = 1

    def __init__(self):
        super().__init__("Footguards")

