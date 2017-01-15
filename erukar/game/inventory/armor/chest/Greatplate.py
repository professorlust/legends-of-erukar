from erukar.engine.inventory.Armor import Armor

class Greatplate(Armor):
    EquipmentLocations = ['chest']
    BaseName="Greatplate"
    Probability = 1

    BaseWeight = 30.0
    BasePrice = 400
    InventoryDescription = "Greatplates are the heaviest standard platemail available on the market, providing extreme protection despite being heavy and expensive."

    def __init__(self):
        super().__init__("Greatplate")
