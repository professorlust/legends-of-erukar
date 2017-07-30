# Quantity dictates how many of this ammunition are in this bundle
# Unlike most AmmoMods, this modifier is only for unowned stacks and is removed when the ammo is picked up
import random

class Quantity:
    ShouldRandomizeOnApply = True
    PersistentAttributes = ['InventoryDescription', 'InventoryName']

    MaxLevel = 6

    # Quantity is randomized from 1 to 2^level
    def randomize(self, paramters=None):
        if not hasattr(self, 'level'):
            self.level = int(random.uniform(0, self.MaxLevel+1))
        self.quantity = int(self.uniform(1, pow(2, self.level)))
