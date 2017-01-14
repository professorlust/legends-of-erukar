from erukar.engine.inventory.Armor import Armor

class Plackart(Armor):
    EquipmentLocations = ['chest']
    BaseName="Plackart"
    Probability = 1
    BaseWeight = 7.2

    def __init__(self):
        super().__init__("Plackart")
