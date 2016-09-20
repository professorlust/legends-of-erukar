from erukar.engine.inventory.ChestArmor import ChestArmor

class Piece(ChestArmor):
    BaseName="Piece"
    Probability = 1

    def __init__(self):
        super().__init__("Piece")
        self.armor_class_modifier = 5
        self.max_dex_mod = 20
