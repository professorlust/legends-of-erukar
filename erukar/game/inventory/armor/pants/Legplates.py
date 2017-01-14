from erukar.engine.inventory.Armor import Armor

class Legplates(Armor):
    EquipmentLocations = ['legs']
    BaseName="Legplates"
    Probability = 1
    BaseWeight = 6.5

    def __init__(self):
        super().__init__("Legplates")
