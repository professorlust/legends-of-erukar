from erukar.engine.inventory.Armor import Armor

class Piece(Armor):
    EquipmentLocations = ['chest']
    BaseName="Piece"
    Probability = 1

    BasePrice = 40
    BaseWeight = 3.2
    InventoryDescription = "A chestpiece is intricately forged or worked by a craftsman."

    def __init__(self):
        super().__init__("Piece")
