from erukar.game.modifiers.WeaponMod import WeaponMod
import random

class ChanceOnHitModifier(WeaponMod):
    ChanceToOccur = 0.05

    def on_apply_damage(self, attack_state, command):
        if random.random() <= self.ChanceToOccur:
            self.do_chance_effect(attack_state, command)

    def do_chance_effect(self, attack_state, command):
        pass
