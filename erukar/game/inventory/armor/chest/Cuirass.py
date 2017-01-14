from erukar.engine.inventory.Armor import Armor

class Cuirass(Armor):
    EquipmentLocations = ['chest']
    BaseName="Cuirass"
    Probability = 1

    BaseWeight = 4.0

    def __init__(self):
        super().__init__("Cuirass")
