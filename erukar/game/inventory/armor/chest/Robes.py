from erukar.engine.inventory.Armor import Armor

class Robes(Armor):
    EquipmentLocations = ['chest']
    BaseName="Robes"
    Probability = 1

    InventoryDescription = "Robes are outerwear which are often used by monks and aracanists."
    BasePrice = 10
    BaseWeight = 0.7

    def __init__(self):
        super().__init__("Robes")
