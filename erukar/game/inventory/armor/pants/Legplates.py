from erukar.engine.inventory.Armor import Armor

class Legplates(Armor):
    EquipmentLocations = ['legs']
    BaseName="Legplates"
    Probability = 1

    def __init__(self):
        super().__init__("Legplates")
        self.armor_class_modifier = 0
        self.max_dex_mod = 20
