from erukar.engine.inventory.Armor import Armor

class Gloves(Armor):
    EquipmentLocations = ['arms']
    BaseName="Gloves"
    Probability = 1
    BaseWeight = 0.5

    def __init__(self):
        super().__init__("Gloves")
