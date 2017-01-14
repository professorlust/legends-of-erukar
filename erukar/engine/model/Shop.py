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
            return 'Insufficient funds (missing {} riphons).'.format(item.price() - purchaser.wealth)
        
        purchaser.wealth -= item.price()
        if self.has_infinite_supply:
            item = Shop.duplicate(item)
        else:
            self.inventory.remove(item)

        purchaser.inventory.append(item)
        item.on_take(purchaser)
        return 'Successfully purchased {} for {} riphons.'.format(item.format(), item.price())

    def buy_from_seller(self, item, seller):
        seller.inventory.remove(item)
        seller.wealth += item.price()
        self.inventory.append(item)
        return 'Successfully sold {} for {} riphons.'.format(item.format(), item.price())

    def duplicate(item):
        return copy.deepcopy(item)
