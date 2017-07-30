from erukar.system.engine import Condition

class DamageOverTime(Condition):
    IsTemporary = True
    Duration = 4 # In ticks, where a tick is 5 seconds
    Incapacitates = False

    Noun        = 'Damage Over Time'
    Participle  = 'Damaging Over Time'
    Description = 'Applies specific Damage every 5 seconds'

    def __init__(self, target, instigator=None):
        super().__init__(target, instigator)
        self.damage = []
        self.damage_efficacy = 1.0
        self.affects_dying = False

    def do_tick_effect(self):
        if self.target.has_condition(erukar.engine.conditions.Dead): return
        if self.target.has_condition(erukar.engine.conditions.Dying) and not self.affects_dying: return
    
        result = self.target.process_damage(self.damage, self.instigator, self.damage_efficacy)
#        a_res, self_res = MagicDamageFormatter.get_string_results(result)
#       print('\n'.join(a_res))
#       print('\n'.join(self_res))
#       return '\n'.join(self_res)
