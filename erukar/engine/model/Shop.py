class Shop:
    def __init__(self, total_wealth):
        self.inventory = []
        self.total_wealth = total_wealth


    def create(item_type, material_type):
        item = item_type()
        material_type().apply_to(item)
        return item

    def display_inventory(self):
        for i, item in enumerate(self.inventory):
            yield '{:3} -- {}'.format(i, item.format())
