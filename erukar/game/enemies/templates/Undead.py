from erukar.engine.lifeforms.Enemy import Enemy
import erukar

class Undead(Enemy):
    def __init__(self, name, random=True):
        super().__init__(name, random)
        self.conditions.append(erukar.game.conditions.magical.Undead(self))
