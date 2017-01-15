from erukar.engine.inventory.Armor import Armor

class Vambrace(Armor):
    EquipmentLocations = ['arms']
    BaseName="Vambrace"
    Probability = 1

    InventoryDescription = "Vambrace todo"
    BasePrice = 60
    BaseWeight = 2.0

    def __init__(self):
        super().__init__("Vambrace")
