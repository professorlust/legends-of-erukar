from erukar.engine.inventory.Armor import Armor

class Sprinters(Armor):
    EquipmentLocations = ['feet']
    BaseName="Sprinters"
    Probability = 1

    def __init__(self):
        super().__init__("Sprinters")
        self.armor_class_modifier = 0
        self.max_dex_mod = 20


