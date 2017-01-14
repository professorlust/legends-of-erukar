from erukar.engine.inventory.Armor import Armor

class Sabatons(Armor):
    EquipmentLocations = ['feet']
    BaseName="Sabatons"
    Probability = 1
    BaseWeight = 4.0

    def __init__(self):
        super().__init__("Sabatons")

