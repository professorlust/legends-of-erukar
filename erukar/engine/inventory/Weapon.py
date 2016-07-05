from .Item import Item
from erukar.engine.model.Damage import Damage
import numpy as np

class Weapon(Item):
    def __init__(self, name="Weapon"):
        super().__init__("weapon", name)
        self.damages = []

    def roll(self, attacker):
        return [(d.roll(attacker), d.name) for d in self.damages]

    def describe(self):
        return self.name

    def on_inspect(self):
        return '{0} ({1})'.format(self.name, self.damage).strip()
