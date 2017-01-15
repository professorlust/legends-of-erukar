from erukar.engine.inventory.Armor import Armor

class Treads(Armor):
    EquipmentLocations = ['feet']
    BaseName="Treads"
    Probability = 1

    BaseWeight = 1
    InventoryDescription = "Treads are specialized boots meant to maintain traction on difficult terrain. They offer a reasonable amount of protection, though perhaps less so than standard boots."
    BasePrice = 15

    def __init__(self):
        super().__init__("Treads")
