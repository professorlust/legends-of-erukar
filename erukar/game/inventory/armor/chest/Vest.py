from erukar.engine.inventory.Armor import Armor

class Vest(Armor):
    EquipmentLocations = ['chest']
    BaseName="Vest"
    Probability = 1
    BaseWeight = 1.5

    def __init__(self):
        super().__init__("Vest")
