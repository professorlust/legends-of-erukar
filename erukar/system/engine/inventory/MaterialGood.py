from .StackableItem import StackableItem

class MaterialGood(StackableItem):
    Persistent = True
    IsUsable = False
    BasePricePerSingle = 0
    WeightPerSingle = 1

    def __init__(self, quantity=1, modifiers=None):
        super().__init__(self.BaseName, quantity, modifiers)

    def price(self, econ=None):
        return self.BasePricePerSingle * econ.price_scalar(self)

    def base_price(self):
        return self.BasePricePerSingle

    def total_weight(self):
        return self.WeightPerSingle * self.quantity
