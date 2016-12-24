from erukar.engine.model.Condition import Condition
import erukar

class Hemorrhaging(Condition):
    IsTemporary = True
    Duration = 12 # In ticks, where a tick is 5 seconds
    Incapacitates = False
    strength = -5
    dexterity = -5
    vitality = -5

    def __init__(self, target, instigator=None):
        super().__init__(target, instigator)
        damage = Damage(
            'bleeding',
            (1, 4),
            '',
            (random.random, (0,1)))

    def do_tick_effect(self):
        xp = self.target.apply_damage(damage, self.instigator)
        if xp and self.instigator:
            self.instigator.award_xp(xp, self.target)
