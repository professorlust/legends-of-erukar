from erukar.engine.inventory.Item import Item
import numpy as np

class Weapon(Item):
    def __init__(self, name="Weapon"):
        super().__init__("weapon", name)
        self.damage_range = (0, 1)
        self.damage_modifier = 'str'
        self.distribution = np.random.beta
        self.random_params = (1, 1)

    def roll(self):
        random_val = self.distribution(*self.random_params)
        return (self.damage_range[1] - self.damage_range[0]) * round(random_val) + self.damage_range[0]

    def describe(self):
        return self.name

    def on_inspect(self):
        return '{0} ({1})'.format(self.name, self.damage).strip()
