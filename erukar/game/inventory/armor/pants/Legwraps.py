from erukar.engine.inventory.Armor import Armor

class Legwraps(Armor):
    EquipmentLocations = ['legs']
    BaseName="Legwraps"
    Probability = 1
    BaseWeight = 0.7

    def __init__(self):
        super().__init__("Legwraps")
