from erukar.game.modifiers.WeaponMod import WeaponMod
import erukar

class Bane(WeaponMod):
    TargetType = 'Undead'

    def __init__(self):
        super().__init__()
        self.target_type = getattr(erukar.game.enemies.templates, self.TargetType)

    def on_apply_damage(self, attack_state, command):
        if isinstance(attack_state.target, self.target_type):
            self.do_target_effect(attack_state, command)

    def do_target_effect(self, attack_state, command):
        pass
