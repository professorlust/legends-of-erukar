from erukar.engine.inventory.Armor import Armor

class Mantle(Armor):
    EquipmentLocations = ['chest']
    BaseName="Mantle"
    Probability = 1

    def __init__(self):
        super().__init__("Mantle")
        self.equipment_locations = ['chest']
        self.armor_class_modifier = 2
        self.max_dex_mod = 20
