from .Item import Item

class StackableItem(Item):
    Persistent = True
    PersistentAttributes = ['quantity']
    MaximumStackQuantity = 100

    def __init__(self, name, quantity=1, modifiers=None):
        super().__init__(name, name, modifiers=modifiers)
        self.quantity = quantity

    def on_take(self, lifeform):
        '''On Take here handles stacking'''
        super().on_take(lifeform)

        # Check to see if there's an existing stack that isn't full
        existing_stack = next(self.other_stacks(lifeform.inventory), None)
        # if there is one, add our quantity to that quantity
        if existing_stack is not None:
            existing_stack.quantity += self.quantity

            # If we were able to put everything in the existing stack, remove this item and leave
            if existing_stack.quantity <= self.MaximumStackQuantity:
                lifeform.inventory.remove(self)
                return

            # We have exceeded the max, so split the difference and make a new stack
            difference = existing_stack.quantity - self.MaximumStackQuantity
            self.quantity = difference
            existing_stack.quantity = self.MaximumStackQuantity

    def long_alias(self):
        if self.quantity <= 1: return super().alias()
        return '{} x{}'.format(super().alias(), self.quantity)

    def other_stacks(self, inventory):
        for item in inventory:
            if self.can_stack_on(item): 
                yield item

    def can_stack_on(self, other):
        return type(other) == type(self)\
                and other is not self\
                and self.matches_modifiers(other)\
                and other.quantity < self.MaximumStackQuantity

    def matches_modifiers(self, other):
        return len(self.modifiers) == len(other.modifiers)\
                and type(self.material) == type(other.material)\
                and all(other.has_modifier(type(modifier)) for modifier in self.modifiers)

    def has_modifier(self, material_type):
        return material_type in [type(y) for y in self.modifiers]

    def on_inventory(self):
        if self.quantity <= 1: return self.format()
        return '{} x{}'.format(self.format(), self.quantity)

    def consume(self):
        self.quantity -= 1
        if self.quantity <= 0:
            self.owner.inventory.remove(self)

    @classmethod
    def split(cls, original, quantity):
        if original.quantity <= 1 or original.quantity <= quantity: 
            return original, None
        original.quantity -= quantity
        split_off = cls.duplicate(original, quantity)
        return split_off, original

    def duplication_args(self, quantity):
        return {
            'quantity': quantity,
            'modifiers': []
        }

    @classmethod
    def duplicate(cls, obj, new_quantity):
        return cls(**obj.duplication_args(new_quantity))

