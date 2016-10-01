from erukar.engine.inventory.Item import Item

class Armor(Item):
    EquipmentLocations = ['chest']
    Persistent = True
    EssentialPart = "armor"

    def __init__(self, name="Armor"):
        super().__init__("armor", name)
        self.armor_class_modifier = 2
        self.max_dex_mod = 2

    def calculate_armor_class(self):
        return self.armor_class_modifier
