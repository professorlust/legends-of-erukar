from erukar.engine.inventory.Armor import Armor

class Footguards(Armor):
    EquipmentLocations = ['feet']

    BaseName="Footguards"
    InventoryDescription = "Basic footgear which aims to protect the soles of the feet and provide a small amount of protection from debris, caltrops, and other obstructions laying about"

    BasePrice = 15
    BaseWeight = 1.5
    Probability = 1

    def __init__(self):
        super().__init__("Footguards")

