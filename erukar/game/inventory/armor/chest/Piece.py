from erukar.engine.inventory.Armor import Armor

class Piece(Armor):
    EquipmentLocations = ['chest']
    BaseName="Piece"
    Probability = 1
    BaseWeight = 3.2

    def __init__(self):
        super().__init__("Piece")
