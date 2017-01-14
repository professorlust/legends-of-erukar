from erukar.engine.inventory.Armor import Armor

class Raiment(Armor):
    EquipmentLocations = ['chest']
    BaseName="Raiment"
    Probability = 1
    BaseWeight = 0.8

    def __init__(self):
        super().__init__("Raiment")
