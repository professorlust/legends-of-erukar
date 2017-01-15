from erukar.engine.inventory.Armor import Armor

class Shroud(Armor):
    EquipmentLocations = ['chest']
    BaseName="Shroud"
    Probability = 1

    BasePrice = 15
    InventoryDescription = "Shroud todo"
    BaseWeight = 0.75

    def __init__(self):
        super().__init__("Shroud")
