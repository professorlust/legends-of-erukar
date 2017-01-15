from erukar.engine.inventory.Armor import Armor

class Warboots(Armor):
    EquipmentLocations = ['feet']
    BaseName="Warboots"
    Probability = 1

    BasePrice = 50.0
    InventoryDescription = "Heavily armored footgear traditionally used by heavy knights. Provides a lot of protection at the cost of maneuverability."
    BaseWeight = 5.7

    def __init__(self):
        super().__init__("Warboots")
