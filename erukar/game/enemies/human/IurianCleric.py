from erukar.engine.lifeforms.Enemy import Enemy
import erukar, random

class IurianCleric(Enemy):
    BriefDescription = "an Iurian Cleric"
    RandomizedArmor = [
        ('left', 'erukar.game.inventory.armor.shields'),
        ('feet', 'erukar.game.inventory.armor.chest'),
        ('chest', 'erukar.game.inventory.armor.boots'),
        ('head', 'erukar.game.inventory.armor.helm')
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
        self.spells = [erukar.game.magic.predefined.Heal()]
        self.define_level(5)
        self.randomize_equipment()

    def perform_turn(self):
        if self.health < (self.max_health / 2):
            return self.heal_self()
        targets = list(self.viable_targets(self.current_room))
        if len(targets) > 0:
            return self.do_attack(targets)
        return self.maybe_move_somewhere()

    def heal_self(self):
        cast = erukar.engine.commands.executable.Cast()
        cast.sender_uid = self.uid
        cast.user_specified_payload = 'Heal'
        return cast
