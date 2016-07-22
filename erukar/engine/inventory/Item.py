from erukar.engine.model.RpgEntity import RpgEntity

class Item(RpgEntity):
    generic_description = 'This is {0}, but it otherwise has no real description whatsoever'

    def __init__(self, item_type='Item', name="Item"):
        self.item_type = item_type
        self.equipment_locations = []
        self.name = name
        self.price = 0
        self.description = Item.generic_description

    def describe(self):
        return self.alias()

    def matches(self, other):
        return other.lower() in self.alias().lower() \
            or other.lower() in self.item_type.lower()

    def on_inspect(self, *_):
        return self.description.format(self.name)

    def on_inventory(self, *_):
        return self.alias()

    def alias(self):
        return self.name

    def belongs_in_hand(self):
        return 'left' in self.equipment_locations or 'right' in self.equipment_locations
