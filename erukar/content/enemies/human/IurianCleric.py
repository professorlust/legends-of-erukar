from erukar.system.engine import Enemy
import erukar, random

class IurianCleric(Enemy):
    BriefDescription = "an Iurian Cleric"
    RandomizedArmor = [
        ('left', 'erukar.content.inventory.armor.shields'),
        ('feet', 'erukar.content.inventory.armor.chest'),
        ('chest', 'erukar.content.inventory.armor.boots'),
        ('head', 'erukar.content.inventory.armor.helm')
    ]
    RandomizedWeapons = ['right' ]

    def __init__(self, random=True):
        super().__init__("Iurian Cleric")
        # The 
        self.str_ratio = 0.2
        self.dex_ratio = 0.1
        self.vit_ratio = 0.1
        self.acu_ratio = 0.1
        self.sen_ratio = 0.3
        self.res_ratio = 0.2
        self.define_level(5)
        self.randomize_equipment()

    def perform_turn(self):
        targets = list(self.viable_targets(self.current_room))
        if len(targets) > 0:
            return self.do_attack(targets)
        return self.maybe_move_somewhere()
