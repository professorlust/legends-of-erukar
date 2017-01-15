from erukar.engine.inventory.Armor import Armor

class Legplates(Armor):
    EquipmentLocations = ['legs']
    BaseName="Legplates"
    Probability = 1
    
    InventoryDescription = "Legplates are heavier than greaves but offer slightly better protection."
    BasePrice = 100
    BaseWeight = 6

    def __init__(self):
        super().__init__("Legplates")
