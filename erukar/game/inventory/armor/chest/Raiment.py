from erukar.engine.inventory.Armor import Armor

class Raiment(Armor):
    EquipmentLocations = ['chest']
    BaseName="Raiment"
    Probability = 1

    InventoryDescription = "Raiments are stylish jerkins which provide next to no real protection but offer plenty of mobility"
    BaseWeight = 0.8
    BasePrice = 15

    def __init__(self):
        super().__init__("Raiment")
