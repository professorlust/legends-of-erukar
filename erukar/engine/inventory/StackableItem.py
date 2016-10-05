from .Item import Item

class StackableItem(Item):
    Persistent = True
    PersistentAttributes = ['quantity']
    MaximumStackQuantity = 100

    def __init__(self, name, quantity=1):
        super().__init__(name, name)
        self.quantity = quantity

    def on_take(self, lifeform):
        existing_stack = next(self.other_stacks(lifeform.inventory), None)
        if existing_stack:
            existing_stack.quantity += self.quantity
            if existing_stack.quantity <= self.MaximumStackQuantity:
                lifeform.inventory.remove(self)
                return
            difference = existing_stack.quantity - self.MaximumStackQuantity
            self.quantity = difference
            existing_stack.quantity = self.MaximumStackQuantity

    def other_stacks(self, inventory):
        for item in inventory:
            if type(item) == type(self) and item is not self and item.quantity < self.MaximumStackQuantity:
                yield item

    def on_inventory(self):
        return '{} x{}'.format(self.name, self.quantity)
