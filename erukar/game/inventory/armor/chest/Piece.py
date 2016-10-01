from erukar.engine.inventory.Armor import Armor

class Piece(Armor):
    EquipmentLocations = ['chest']
    BaseName="Piece"
    Probability = 1

    def __init__(self):
        super().__init__("Piece")
        self.armor_class_modifier = 5
        self.max_dex_mod = 20
