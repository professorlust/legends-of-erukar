from .Item import Item

class StackableItem(Item):
    Persistent = True
    PersistentAttributes = ['quantity']
    MaximumStackQuantity = 100

    def __init__(self, name, quantity=1):
        super().__init__(name, name)
        self.quantity = quantity

    def on_take(self, lifeform):
        '''On Take here handles stacking'''
        super().on_take(lifeform)

        # Check to see if there's an existing stack that isn't full
        existing_stack = next(self.other_stacks(lifeform.inventory), None)
        # if there is one, add our quantity to that quantity
        if existing_stack:
            existing_stack.quantity += self.quantity

            # If we were able to put everything in the existing stack, remove this item and leave
            if existing_stack.quantity <= self.MaximumStackQuantity:
                lifeform.inventory.remove(self)
                return

            # We have exceeded the max, so split the difference and make a new stack
            difference = existing_stack.quantity - self.MaximumStackQuantity
            self.quantity = difference
            existing_stack.quantity = self.MaximumStackQuantity


    def other_stacks(self, inventory):
        for item in inventory:
            if type(item) == type(self) and item is not self and item.quantity < self.MaximumStackQuantity:
                yield item

    def on_inventory(self):
        return '{} x{}'.format(self.name, self.quantity)

    def consume(self):
        self.quantity -= 1
        if self.quantity <= 0:
            self.owner.inventory.remove(self)
