from erukar.system.engine import Condition, Damage
import random

class Enraged(Condition):
    IsTemporary = True
    Duration = 4 # In ticks, where a tick is 5 seconds
    Incapacitates = False
    
    Noun        = 'Enraged'
    Participle  = 'Raging'
    Description = 'Adds Total Resolve Score to attack rolls, physical damage, and physical mitigation but reduces sense and acuity by the same amount'

    def __init__(self, target, instigator=None):
        super().__init__(target, instigator)
        if instigator is None:
            instigator = target
        self.resolve_score = instigator.calculate_effective_stat('resolve')
        self.DamageMitigations = {
            'bludgeoning': (0, self.resolve_score),
            'piercing': (0, self.resolve_score),
            'slashing': (0, self.resolve_score)
        }

    def modify_acuity(self):
        return -self.resolve_score

    def modify_sense(self):
        return -self.resolve_score

    def modify_attack_roll(self, target):
        return self.resolve_score

    def on_process_damage(self, attack_state, command):
        extra_damage = self.resolve_score
        damage = Damage(
            "force",
            (extra_damage, extra_damage),
            'resolve',
            dist_and_params=(random.uniform, (0,1))
        )
        attack_state.add_extra_damage([damage])
