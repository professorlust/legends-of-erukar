from erukar.engine.inventory.Armor import Armor

class Treads(Armor):
    EquipmentLocations = ['feet']
    BaseName="Treads"
    Probability = 1

    BaseWeight = 1

    def __init__(self):
        super().__init__("Treads")
