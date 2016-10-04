from .Item import Item

class StackableItem(Item):
    Persistent = True
    PersistentAttributes = ['quantity']

    def __init__(self, name, quantity=1):
        super().__init__(name, name)
        self.quantity = quantity

    def on_take(self, lifeform):
        existing_stack = next(self.other_stacks(lifeform.inventory), None)
        if existing_stack:
            existing_stack.quantity += self.quantity
            lifeform.inventory.remove(self)

    def other_stacks(self, inventory):
        for item in inventory:
            if type(item) == type(self) and item is not self:
                yield item

    def on_inventory(self):
        return '{} x{}'.format(self.name, self.quantity)
