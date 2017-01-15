from erukar.engine.inventory.Armor import Armor

class Sprinters(Armor):
    EquipmentLocations = ['feet']
    BaseName="Sprinters"
    Probability = 1

    InventoryDescription = "An advanced shoe specifically crafted to provide some protection yet still allow a large degree of movement."
    BaseWeight = 0.5
    BasePrice = 20

    def __init__(self):
        super().__init__("Sprinters")
