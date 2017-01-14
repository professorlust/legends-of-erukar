from erukar.engine.inventory.Armor import Armor

class Warboots(Armor):
    EquipmentLocations = ['feet']
    BaseName="Warboots"
    Probability = 1
    BaseWeight = 5.7

    def __init__(self):
        super().__init__("Warboots")
