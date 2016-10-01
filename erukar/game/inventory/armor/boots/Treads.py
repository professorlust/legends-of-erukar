from erukar.engine.inventory.Armor import Armor

class Treads(Armor):
    EquipmentLocations = ['feet']
    BaseName="Treads"
    Probability = 1

    def __init__(self):
        super().__init__("Treads")
        self.armor_class_modifier = 0
        self.max_dex_mod = 20


