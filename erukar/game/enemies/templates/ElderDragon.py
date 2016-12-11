from erukar.game.enemies.templates.Dragon import Dragon
import erukar, random

class ElderDragon(Dragon):
    def __init__(self, actual_name):
        super().__init__(actual_name)
        self.strength   = int(random.uniform(6, 8))
        self.dexterity  = int(random.uniform(3, 8))
        self.vitality   = int(random.uniform(6, 9))
        self.acuity     = int(random.uniform(4, 9))
        self.sense      = int(random.uniform(4, 9))
        self.resolve    = int(random.uniform(10, 13))
        self.name = actual_name
