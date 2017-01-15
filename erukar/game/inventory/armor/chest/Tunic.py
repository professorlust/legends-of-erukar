from erukar.engine.inventory.Armor import Armor

class Tunic(Armor):
    EquipmentLocations = ['chest']
    BaseName="Tunic"
    Probability = 1

    InventoryDescription = "Tunic todo"
    BasePrice = 30
    BaseWeight = 1.0

    def __init__(self):
        super().__init__("Tunic")
