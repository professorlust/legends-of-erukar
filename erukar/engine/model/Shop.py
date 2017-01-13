import copy

class Shop:
    def __init__(self, total_wealth):
        self.inventory = []
        self.has_infinite_supply = False
        self.total_wealth = total_wealth

    def create(item_type, material_type):
        item = item_type()
        material_type().apply_to(item)
        return item

    def display_inventory(self):
        for i, item in enumerate(self.inventory):
            yield '{:3} -- {}'.format(i+1, item.format(with_price=True))

    def sell_to_buyer(self, item, purchaser):
        if not item in self.inventory: 
            return '{} is not in stock'.format(item.format())

        if purchaser.wealth < item.price():
            return 'Insufficient funds.'
        
        purchaser.wealth -= item.price()
        if self.has_infinite_supply:
            purchaser.inventory.append(Shop.duplicate(item))
        else:
            self.inventory.remove(item)
            purchaser.inventory.append(item)
        return 'Successfully purchased {}'.format(item.format())

    def buy_from_seller(self, item, seller):
        seller.inventory.remove(item)
        seller.wealth += item.price()
        self.inventory.append(item)

    def duplicate(item):
        return copy.deepcopy(item)
