from erukar.engine.inventory.Armor import Armor

class Sabatons(Armor):
    EquipmentLocations = ['feet']
    BaseName="Sabatons"
    Probability = 1

    InventoryDescription = "Highly protective, armored footgear which is often part of a platemail suit. Provides a large amount of protection around all sides of the feet."
    BasePrice = 40
    BaseWeight = 4.0

    def __init__(self):
        super().__init__("Sabatons")

