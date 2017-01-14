from erukar.engine.inventory.Armor import Armor

class Mantle(Armor):
    EquipmentLocations = ['chest']
    BaseName="Mantle"
    Probability = 1
    BaseWeight = 1.5

    def __init__(self):
        super().__init__("Mantle")
