from erukar.engine.inventory.Armor import Armor

class Guard(Armor):
    EquipmentLocations = ['chest']
    BaseName="Guard"
    Probability = 1

    BaseWeight = 5.0
    BasePrice = 50
    InventoryDescription = "Guard description todo"

    def __init__(self):
        super().__init__("Guard")
