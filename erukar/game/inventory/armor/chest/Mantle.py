from erukar.engine.inventory.Armor import Armor

class Mantle(Armor):
    EquipmentLocations = ['chest']
    BaseName="Mantle"
    Probability = 1

    BaseWeight = 1.5
    BasePrice = 30
    InventoryDescription = "Mantles are loose fitting pieces that cover the torso. What they lack in protection they certainly make up in style."

    def __init__(self):
        super().__init__("Mantle")
