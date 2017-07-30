from erukar.system.engine import Enemy
from erukar.content.conditions import Undead
import random

class Lich(Enemy):
    BriefDescription = "a lich  "

    def __init__(self, random=True):
        super().__init__("Lich", random)
        # Now personality
        self.str_ratio = 0.05
        self.dex_ratio = 0.1
        self.vit_ratio = 0.05
        self.acu_ratio = 0.4
        self.sen_ratio = 0.25
        self.res_ratio = 0.15
        self.define_level(40)
        self.spells = [
        ]
        self.conditions.append(Undead(self))

    def perform_turn(self):
        targets = list(self.viable_targets(self.current_room))
        return self.maybe_move_somewhere()
