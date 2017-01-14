from erukar.engine.inventory.Armor import Armor

class Spurs(Armor):
    EquipmentLocations = ['feet']
    BaseName="Spurs"
    Probability = 1
    BaseWeight = 1.5

    def __init__(self):
        super().__init__("Spurs")
