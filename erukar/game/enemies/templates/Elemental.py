from erukar.engine.lifeforms.Enemy import Enemy
import erukar, random

class Elemental(Enemy):
    def __init__(self, actual_name, is_random=True):
        super().__init__(actual_name, is_random)
        self.resolve   = 5
        self.sense     = -2
        self.acuity    = -4
        # Now personality
        self.str_ratio = 0.23333
        self.dex_ratio = 0.23333
        self.vit_ratio = 0.23333
        self.acu_ratio = 0
        self.sen_ratio = 0
        self.res_ratio = 0.3
        self.define_level(10)
        
        self.left = erukar.game.inventory.weapons.enemy.Claws()
        self.right = erukar.game.inventory.weapons.enemy.Claws()
