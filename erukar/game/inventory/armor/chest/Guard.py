from erukar.engine.inventory.Armor import Armor

class Guard(Armor):
    EquipmentLocations = ['chest']
    BaseName="Guard"
    Probability = 1

    def __init__(self):
        super().__init__("Guard")
        self.equipment_locations = ['chest']
        self.armor_class_modifier = 8
        self.max_dex_mod = 20
