class Shop:
    def __init__(self, total_wealth):
        self.inventory = []
        self.total_wealth = total_wealth

    def format_item(item):
        if hasattr(item, 'material') and item.material:
            return '{} {} ({} R)'.format(item.material.InventoryName, item.alias(), int(item.price()))
        return '{} ({} R)'.format(item.alias(), int(item.price()))

    def create(item_type, material_type):
        item = item_type()
        material_type().apply_to(item)
        return item

    def display_inventory(self):
        for i, item in enumerate(self.inventory):
            yield '{:3} -- {}'.format(i, Shop.format_item(item))
