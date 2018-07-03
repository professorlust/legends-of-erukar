from erukar.system.engine import Enemy
import erukar


class Undead(Enemy):
    def __init__(self, name='', random=True):
        super().__init__(name, random)
        erukar.content.conditions.magical.Undead(self)
