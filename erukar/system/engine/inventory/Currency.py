from .StackableItem import StackableItem
import random

class Currency(StackableItem):
    def __init__(self):
        super().__init__('currency', int(random.uniform(10, 100)))
        self.item_type = "currency"
        self.name = "currency"
