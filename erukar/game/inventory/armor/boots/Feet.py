from erukar.engine.inventory.Armor import Armor

class Feet(Armor):
    EquipmentLocations = ['feet']
    '''Note: This requires a magical modifier!'''
    Probability = 1
    BaseName = "Feet"

    def __init__(self):
        super().__init__("Feet")
