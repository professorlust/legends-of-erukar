from erukar.engine.model.Condition import Condition
import erukar

class DamageOverTime(Condition):
    IsTemporary = True
    Duration = 4 # In ticks, where a tick is 5 seconds
    Incapacitates = False

    def __init__(self, target, instigator=None):
        super().__init__(target, instigator)
        self.damage = []
        self.damage_efficacy = 1.0
        self.affects_dying = False

    def do_tick_effect(self):
        if self.target.has_condition(erukar.engine.conditions.Dead): return
        if self.target.has_condition(erukar.engine.conditions.Dying) and not self.affects_dying: return
    
        result = self.target.apply_damage(self.damage, self.instigator, self.damage_efficacy)
        MagicalDamageFormatter.process_and_append_damage_result(self.cmd, result)
