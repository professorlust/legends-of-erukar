from erukar.game.modifiers.inventory.base.Bane import Bane
from erukar.engine.model.Damage import Damage
import random

class UndeadBane(Bane):
    Probability = 1
    Desirability = 8.0
    TargetType = 'Undead'

    DamageIncrease = 0.25
    InventoryDescription = "Deals 25% extra damage against undead creatures"
    InventoryName = "Undead Bane"

    def do_target_effect(self, attack_state, command):
        extra_damage = attack_state.damage_result.get_damage_total() * self.DamageIncrease
        damage = Damage(
            "unmitigable",
            (extra_damage, extra_damage),
            'resolve',
            dist_and_params=(random.uniform, (0,1))
        )
        attack_state.add_extra_damage([damage])
